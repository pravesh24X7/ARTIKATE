import pandas as pd


# returns the synthetic dataset in list format
def get_synthetic_dataset():
    data = [
        {"text": "I was charged twice", "labels": 0},  # billing
        {"text": "Button not working", "labels": 1},   # technical
        {"text": "Add dark mode", "labels": 2},        # feature
        {"text": "Very bad service", "labels": 3},     # complaint
        {"text": "Hello", "labels": 4},                # other
    ] * 200

    return data


# returns the synthetic dataset in pd.DataFrame object.
def get_synthetic_dataset_df() -> pd.DataFrame:
    return pd.DataFrame(get_synthetic_dataset())
