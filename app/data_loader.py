import pandas as pd


FILE_PATH = r"data/raw/executive_finance_raw_dirty.csv"

def load_data():
    df = pd.read_csv(FILE_PATH)
    return df
