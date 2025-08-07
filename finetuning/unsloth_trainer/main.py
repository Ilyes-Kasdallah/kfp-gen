from unsloth import FastLanguageModel
from trl import PPOTrainer, PPOConfig
from datasets import load_dataset
from tokenizer_utils import load_tokenizer
from reward_model import total_reward

model_name = "Qwen/Qwen2.5-7B-Instruct"
tokenizer = load_tokenizer(model_name)
model, _ = FastLanguageModel.from_pretrained(model_name, load_in_4bit=True, use_unsloth=True)
model = FastLanguageModel.get_peft_model(model, r=8, target_modules=["q_proj", "v_proj"])

dataset = load_dataset("json", data_files="data/prompts_dataset.jsonl", split="train")

def format_input(example):
    return {"query": example["prompt"], "response": example["completion"]}

dataset = dataset.map(format_input)

config = PPOConfig(model_name=model_name, learning_rate=1e-5, batch_size=1, mini_batch_size=1, log_with="tensorboard")
ppo_trainer = PPOTrainer(config=config, model=model, tokenizer=tokenizer, dataset=dataset)

for batch in dataset:
    prompt, reference = batch["query"], batch["response"]
    response = ppo_trainer.model.generate(tokenizer(prompt, return_tensors="pt").input_ids, max_new_tokens=1024)
    decoded = tokenizer.decode(response[0], skip_special_tokens=True)
    reward = total_reward(decoded, reference)
    ppo_trainer.step([prompt], [decoded], [reward])
