"""
The following is our RoBERTa script for training our LLM on Kremlin article data. This version of the script runs
strictly on CPU. Model is saved to a model.safetensors file and evaluation metrics saved to evaluation_metrics.json.

The current version of the model is running on out-the-box settings, fine-tuning is still needed.
"""

import pandas as pd
import json
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from transformers import (RobertaConfig, RobertaModel, RobertaTokenizer, AutoTokenizer,
                          RobertaForSequenceClassification, Trainer, TrainingArguments)

file = 'data.csv'
wise_panda = pd.read_csv(file)  # Panda is very wise having read many articles

configuration = RobertaConfig()  # initialize configuration
model = RobertaForSequenceClassification.from_pretrained("FacebookAI/roberta-base")

training_data, testing_data = train_test_split(wise_panda, test_size=0.1, stratify=wise_panda["Disinformation"])
training_data = Dataset.from_pandas(training_data)
testing_data = Dataset.from_pandas(testing_data)

tokenizer = RobertaTokenizer.from_pretrained("FacebookAI/roberta-base")


def tokenize(batch):
    return tokenizer(batch["Translated"], padding="max_length", truncation=True, max_length=512)


training_data = training_data.map(tokenize, batched=True)
testing_data = testing_data.map(tokenize, batched=True)
training_data = training_data.rename_column("Disinformation", "labels")
testing_data = testing_data.rename_column("Disinformation", "labels")
training_data.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
testing_data.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

training_args = TrainingArguments(
    output_dir="./",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=4,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    use_cpu=False
)


def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds),
    }


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=training_data,
    eval_dataset=testing_data,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()
results = trainer.evaluate()

# Saves results
with open('evaluation_metrics.json', 'w') as f:
    json.dump(results, f, indent=4)

model.save_pretrained("./")
tokenizer.save_pretrained("./")