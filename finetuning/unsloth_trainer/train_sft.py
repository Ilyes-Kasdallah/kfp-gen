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
    set_seed
)
from transformers.trainer import TRAINER_STATE_NAME
from transformers.trainer_utils import get_last_checkpoint
from trl import SFTTrainer, SFTConfig, get_kbit_device_map
from accelerate import Accelerator


def format_prompt(example):
    return f"# Prompt:\n{example['prompt']}\n\n# Pipeline Code:\n{example['completion']}"


def main():
  #  nf4_config = BitsAndBytesConfig(
   #     load_in_4bit=True,
   #     bnb_4bit_quant_type="nf4",
   #     bnb_4bit_use_double_quant=True,
   #     bnb_4bit_compute_dtype=torch.float16,
   #     bnb_4bit_quant_storage=torch.float32,
   # )

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        inference_mode=False,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules="all-linear"
    )

    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        #quantization_config=nf4_config,
        torch_dtype=torch.float16,
        attn_implementation="sdpa",
        local_files_only=True,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    tokenizer.pad_token = tokenizer.eos_token

    dataset = datasets.load_from_disk(args.dataset)
    dataset = dataset.map(lambda x: {"text": format_prompt(x)})

    sft_config = SFTConfig(
        do_train=True,
        per_device_train_batch_size=4,          # was args.batch
        per_device_eval_batch_size=4,
        gradient_accumulation_steps=8,          # effective batch = 32
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={'use_reentrant': False},
        eval_strategy="steps",
        eval_steps=200,                         # less I/O; still frequent enough
        logging_steps=20,
        save_strategy="steps",
        save_steps=200,
        save_total_limit=2,
        learning_rate=1e-4,                     # LoRA usually likes 5e-5–2e-4; 1e-4 is a solid start
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,                      # ~3% warmup is safer than none
        weight_decay=0.01,
        max_grad_norm=1.0,
        num_train_epochs=3,
        max_seq_length=args.context,
        dataset_text_field="text",
        output_dir=args.output_dir,
        run_name=args.run_name,
        report_to="wandb",
        disable_tqdm=False,
        fp16=True,                              # V100 = fp16 (bf16 not supported)
        packing=True,
        group_by_length=True,                   # better packing/throughput
        dataloader_num_workers=4,               # small bump in input pipelining

    )

    trainer = SFTTrainer(
        model=model,
        peft_config=peft_config,
        train_dataset=dataset['train'],
        eval_dataset=dataset['test'],
        args=sft_config,
        tokenizer=tokenizer
    )

    trainer.train(resume_from_checkpoint=args.resume)
    trainer.save_model(f"{args.output_dir}/final-model")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Path or HuggingFace ID of the base model")
    parser.add_argument("--dataset", type=str, required=True, help="Path to HuggingFace dataset directory")
    parser.add_argument("--output_dir", type=str, default="./kfp-finetuned", help="Directory to save checkpoints and model")
    parser.add_argument("--run_name", type=str, default="kfp-gen", help="Run name for wandb tracking")
    parser.add_argument("--batch", type=int, default=1, help="Batch size per device")
    parser.add_argument("--grad", type=int, default=4, help="Gradient accumulation steps")
    parser.add_argument("--context", type=int, default=4096, help="Max context length")
    parser.add_argument("--resume", action='store_true', help="Resume training from last checkpoint")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    accelerator = Accelerator(log_with="wandb")
    accelerator.init_trackers(
        'KFP-Finetuning',
        init_kwargs={
            "wandb": {
                "mode": "offline",
                "name": f"exp-{args.run_name}",
                "dir": args.output_dir,
                "resume": "allow" if args.resume else None
            }
        }
    )

    logging.disable_progress_bar()
    datasets.disable_progress_bars()
    set_seed(42)

    main()
    accelerator.end_training()
