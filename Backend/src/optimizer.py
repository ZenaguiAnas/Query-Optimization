# %%
# %%capture
# %pip install accelerate peft bitsandbytes transformers trl

# %%
import os
import torch
from datasets import load_dataset
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import LoraConfig
from trl import SFTTrainer

BASE

# %%
# base_model = "meta-llama/Llama-2-7b-hf"
base_model = "NousResearch/Llama-2-7b-chat-hf"


# New instruction dataset
guanaco_dataset = "mlabonne/guanaco-llama2-1k"

# Fine-tuned model
query_dataset = "queries.csv"

new_model = "llama-2-7b-Neo-Optimizer"

# dataset = load_dataset(guanaco_dataset, split="train")

df = pd.read_csv(query_dataset)
df = Dataset.from_pandas(df)
# dataset = df.train_test_split(test_size=0.1, shuffle=True, seed=42)['train']
dataset = df.train_test_split(test_size=0.1, shuffle=True, seed=42)['train']


# %%
print(dataset)

# %%
compute_dtype = getattr(torch, "float16")

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)

# %%
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=quant_config,
    device_map={"": 0}
)
model.config.use_cache = True
model.config.pretraining_tp = 1

# %%
tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# %%
peft_params = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type="CAUSAL_LM",
)

# %%
training_params = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=1,
    optim="paged_adamw_32bit",
    save_steps=25,
    logging_steps=25,
    learning_rate=2e-4,
    weight_decay=0.001,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="constant",
    report_to="tensorboard"
)

# %%
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_params,
    dataset_text_field="text",
    max_seq_length=None,
    tokenizer=tokenizer,
    args=training_params,
    packing=False,
)

# %%
trainer.model.save_pretrained(new_model)
trainer.tokenizer.save_pretrained(new_model)

# %%
from tensorboard import notebook
log_dir = "results/runs"
notebook.start("--logdir {} --port 4000".format(log_dir))

# %%
logging.set_verbosity(logging.CRITICAL)
prompt="You are a chatbot specializing in optimizing SQL queries within the Oracle syntax ecosystem. Your primary functionality is to provide optimized query.  "
query = "SELECT product_name, AVG(unit_price) as avg_price FROM products GROUP BY category;"
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=400)
result = pipe(f"<s>[INST] {prompt+query} [/INST]")
print(result[0]['generated_text'])


