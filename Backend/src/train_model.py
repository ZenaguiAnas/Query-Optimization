# train_model.py

import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    logging,
)
from peft import LoraConfig
from trl import SFTTrainer

from dotenv import dotenv_values
config = dotenv_values()

QUERY_DATASET = config.get("QUERY_DATASET")
MODEL = config.get("MODEL")
HUB_MODEL_ID = config.get("HUB_MODEL_ID")
HUB_ORGANIZATION = config.get("HUB_ORGANIZATION")
HUB_TOKEN = config.get("HUB_TOKEN")

def train_model():
    # Load the dataset
    dataset = load_dataset(QUERY_DATASET, split="train")

    compute_dtype = getattr(torch, "float16")

    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=False,
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL,
        quantization_config=quant_config,
        device_map={"": 0}
    )
    model.config.use_cache = True
    model.config.pretraining_tp = 1

    tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    peft_params = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=64,
        bias="none",
        task_type="CAUSAL_LM",
    )

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
        report_to="tensorboard",
        push_to_hub=True,
        push_to_hub_model_id=HUB_MODEL_ID,
        push_to_hub_organization=HUB_ORGANIZATION,
        push_to_hub_token=HUB_TOKEN
    )

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

    # trainer.train()
    trainer.model.push_to_hub(repo_id=HUB_MODEL_ID, token=HUB_TOKEN)
    trainer.tokenizer.push_to_hub(repo_id=HUB_MODEL_ID, token=HUB_TOKEN)

if __name__ == "__main__":
    train_model()
