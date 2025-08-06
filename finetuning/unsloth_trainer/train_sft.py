import argparse
import os
from datetime import datetime
import datasets
import torch
from peft import LoraConfig, TaskType
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM
from trl import SFTTrainer, SFTConfig, get_kbit_device_map
from accelerate import Accelerator
from rewards.compute_total_reward import total_reward
from formatting import formatting_func
from tokenizer_utils import load_tokenizer


def main(args_pars):
    # Tokenizer & model
    tokenizer = load_tokenizer(args_pars.model)

    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_storage=torch.float32,
    )

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        inference_mode=False,
        task_type=TaskType.CAUSAL_LM,
        target_modules="all-linear"
    )

    model = AutoModelForCausalLM.from_pretrained(
        args_pars.model,
        quantization_config=nf4_config,
        attn_implementation="sdpa",
        device_map=get_kbit_device_map(),
        torch_dtype=torch.float32,
    )

    if not os.path.exists(args_pars.dataset):
        raise FileNotFoundError(f"Dataset path does not exist: {args_pars.dataset}")

    dataset = datasets.load_from_disk(args_pars.dataset)

    config = SFTConfig(
        per_device_train_batch_size=args_pars.batch,
        per_device_eval_batch_size=args_pars.batch,
        gradient_accumulation_steps=args_pars.grad,
        gradient_checkpointing=True,
        logging_strategy="steps",
        logging_steps=10,
        save_strategy="steps",
        save_steps=50,
        num_train_epochs=3,
        learning_rate=5e-5,
        eval_strategy="steps",
        eval_steps=50,
        output_dir=args_pars.output,
        max_seq_length=args_pars.context,
        dataset_text_field="text",
        packing=True,
        run_name=args_pars.rname,
        report_to="wandb",
        warmup_steps=10,
    )

    trainer = SFTTrainer(
        model=model,
        args=config,
        tokenizer=tokenizer,
        peft_config=peft_config,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        formatting_func=formatting_func
    )

    trainer.train()
    trainer.save_model(args_pars.output)


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--rname", type=str, default="kfp-sft")
    parser.add_argument("--output", type=str, default="./run/kfp_model")
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--grad", type=int, default=4)
    parser.add_argument("--context", type=int, default=2048)
    return parser


if __name__ == "__main__":
    args = setup_parser().parse_args()
    accelerator = Accelerator(log_with="wandb")
    accelerator.init_trackers(
        project_name="kfp-finetuning",
        init_kwargs={"wandb": {"name": args.rname, "mode": "offline"}}
    )
    main(args)
    accelerator.end_training()
