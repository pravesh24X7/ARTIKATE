import torch
import os

from datasets import Dataset
from transformers import (DistilBertTokenizerFast, 
                          DistilBertForSequenceClassification, 
                          Trainer, 
                          TrainingArguments)
from sklearn.model_selection import train_test_split

from src.data.load_data import get_synthetic_dataset


def get_dataset_objects(data):
    return Dataset.from_list(data)


def tokenize(example):
    return tokenizer(example["text"], truncation=True, padding="max_length")


def save_model(model, tokenizer, name):
    os.makedirs("./saved_models", exist_ok=True)
    model.save_pretrained(f"./saved_models/{name}")
    tokenizer.save_pretrained(f"./saved_models/{name}-tokenizer")


if __name__ == "__main__":

    # load the synthetic generated dataset
    data = get_synthetic_dataset()

    # split dataset for training and testing
    train_data, eval_dataset = train_test_split(
        data, test_size=0.2, random_state=24
    )

    # dataset object for train_data and test_data
    train_dataset = get_dataset_objects(train_data)
    eval_dataset = get_dataset_objects(eval_dataset)

    MODEL_NAME = "distilbert-base-uncased"

    # tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

    # apply tokenizer on the dataset
    train_dataset = train_dataset.map(tokenize, batched=True)
    eval_dataset = eval_dataset.map(tokenize, batched=True)

    # create model
    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=5    # already given in problem statement.
    )
    
    # move model to GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device=device)

    print("[+] Training on Device: ", device)

    # defining training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        logging_steps=10,
    )

    trainer = Trainer(model=model,
                      args=training_args,
                      train_dataset=train_dataset,
                      eval_dataset=eval_dataset)

    # begin model training
    trainer.train()

    # save model
    save_model(
        model=model,
        tokenizer=tokenizer,
        name="model001"
    )