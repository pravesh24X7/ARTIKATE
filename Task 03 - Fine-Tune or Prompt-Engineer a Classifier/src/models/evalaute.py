import torch
import time

import numpy as np

from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification


# loads the model from the given path
def load_model_and_tokenizer(model_path):
    model = DistilBertForSequenceClassification.from_pretrained(model_path)
    tokenizer = DistilBertTokenizerFast.from_pretrained(f"{model_path}-tokenizer")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    return model, tokenizer, device


# return the model predictions
def get_predictions(texts, model, tokenizer, device):
    model.eval()

    with torch.no_grad():
        inputs = tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            padding="max_length"
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}

        outputs = model(**inputs)
        preds = torch.argmax(outputs.logits, dim=1)

    return preds


# single prediction
def predict(text, model, tokenizer, device):
    preds = get_predictions([text], model, tokenizer, device)
    return preds.item()


# evaluation using accuracy, f1_score and confusion matrix.
def do_evaluation(texts, labels, model, tokenizer, device):
    preds = get_predictions(texts, model, tokenizer, device).cpu().numpy()

    return {
        "accuracy": accuracy_score(labels, preds),
        "confusion_matrix": confusion_matrix(labels, preds),
        "f1_score": f1_score(labels, preds, average=None)
    }


# latency test, if greater than 500ms, assertion raised
def latency_test(model, tokenizer, device):
    test_inputs = ["Sample ticket"] * 20

    start = time.time()

    for text in test_inputs:
        _ = predict(text, model, tokenizer, device)

    total_time = time.time() - start
    avg_time = total_time / len(test_inputs)

    print("Avg latency per request:", avg_time)

    assert avg_time < 0.5, "Latency exceeds 500ms"


# check the most confusing classes
def most_confused_classes(cm):
    cm = cm.copy()
    np.fill_diagonal(cm, 0)     # ignores correct predictions.

    i, j = np.unravel_index(cm.argmax(), cm.shape)
    return i, j, cm[i, j]

if __name__ == "__main__":

    model, tokenizer, device = load_model_and_tokenizer(
        model_path="./saved_models/model001"
    )

    # using a complex Test dataset
    data = [
        {"text": "App not working", "label": 1},
        {"text": "Very bad app experience", "label": 3},
        {"text": "Payment failed again", "label": 0},
        {"text": "Feature not working properly", "label": 2},
        {"text": "This is bad", "label": 3},
        {"text": "App crashed again", "label": 1},
    ] * 50  # change this to 20

    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]

    # Evaluation
    results = do_evaluation(
        model=model,
        tokenizer=tokenizer,
        device=device,
        texts=texts,
        labels=labels
    )

    print(results)

    # does latency check
    latency_test(model, tokenizer, device)

    # check most confusing classes
    print(most_confused_classes(results["confusion_matrix"]))