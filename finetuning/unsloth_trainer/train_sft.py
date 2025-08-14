import os
import argparse
from datetime import datetime

import torch
import datasets
from peft import LoraConfig, TaskType
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    logging,
    TrainerState,
    set_seed,
)
from transformers.trainer import TRAINER_STATE_NAME
from transformers.trainer_utils import get_last_checkpoint
from trl import SFTTrainer, SFTConfig, get_kbit_device_map
from accelerate import Accelerator


def format_prompt(example):
    return f"# Prompt:\n{example['prompt']}\n\n# Pipeline Code:\n{example['completion']}"


def main(args):
    # ---- Quantization: QLoRA 4-bit on V100 (fp16 compute) ----
    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,   # V100 = fp16
        bnb_4bit_quant_storage=torch.float32,
    )

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        inference_mode=False,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules="all-linear",
    )

    # ---- Model ----
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        quantization_config=nf4_config,
        torch_dtype=torch.float16,           # compute dtype
        attn_implementation="sdpa",          # V100: FA2 not supported; SDPA is efficient
        local_files_only=True,
        device_map="auto",
    )

    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True, use_fast=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # ---- Data ----
    dataset = datasets.load_from_disk(args.dataset)
    dataset = dataset.map(lambda x: {"text": format_prompt(x)})

    # Cap context to something safer by default; you can lift later
    max_ctx = min(args.context, 1024)

    # ---- Training config (NOW honors CLI) ----
    sft_config = SFTConfig(
        do_train=True,
        per_device_train_batch_size=args.batch,
        per_device_eval_batch_size=args.batch,
        gradient_accumulation_steps=args.grad,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},

        evaluation_strategy="steps",
        eval_steps=200,
        logging_steps=20,

        save_strategy="steps",
        save_steps=200,
        save_total_limit=2,

        learning_rate=1e-4,                  # good starting LR for LoRA
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        weight_decay=0.01,
        max_grad_norm=1.0,

        num_train_epochs=3,
        max_seq_length=max_ctx,
        dataset_text_field="text",
        output_dir=args.output_dir,
        run_name=args.run_name,
        report_to="wandb",
        disable_tqdm=False,

        fp16=True,                           # V100 → fp16
        packing=False,                        # start without packing (reduces OOM risk)
        group_by_length=True,                 # better memory use
        dataloader_num_workers=4,
    )

    trainer = SFTTrainer(
        model=model,
        peft_config=peft_config,
        train_dataset=dataset["train"],
        eval_dataset=dataset.get("test", None),
        args=sft_config,
        tokenizer=tokenizer,
    )

    trainer.train(resume_from_checkpoint=args.resume)
    trainer.save_model(f"{args.output_dir}/final-model")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="./kfp-finetuned")
    parser.add_argument("--run_name", type=str, default="kfp-gen")
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--grad", type=int, default=4)
    parser.add_argument("--context", type=int, default=1536)
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    accelerator = Accelerator(log_with="wandb")
    accelerator.init_trackers(
        "KFP-Finetuning",
        init_kwargs={
            "wandb": {
                "mode": "offline",   # change to "online" or export WANDB_MODE=online if you want
                "name": f"exp-{args.run_name}",
                "dir": args.output_dir,
                "resume": "allow" if args.resume else None,
            }
        },
    )

    logging.disable_progress_bar()
    datasets.disable_progress_bars()
    set_seed(42)

    main(args)
    accelerator.end_training()
