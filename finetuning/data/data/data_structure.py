from datasets import load_from_disk
dataset = load_from_disk('/home/ilyes101/Documents/pfe-project/kfp-gen/finetuning/data/data/prompts_dataset')
print(dataset)
print(dataset['train'].column_names)