from fastapi import FastAPI
from app.data_loader import load_data

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API funcionando"}

@app.get("/data/raw")
def get_raw_data(limit: int = 10):
    df = load_data()
    df = df.head(limit)
    df = df.fillna("")
    return df.to_dict(orient="records")


@app.get("/data/filter")
def filter_data(column: str, value: str, limit: int = 10):
    df = load_data()

    if column not in df.columns:
        return {
            "error": f"La columna '{column}' no existe",
            "available_columns": list(df.columns)
        }

    df = df[df[column].astype(str) == value]
    df = df.head(limit)
    df = df.fillna("")

    return df.to_dict(orient="records")

@app.get("/data/summary")
def summary_data(group_by: str, limit: int = 10):
    df = load_data()

    if group_by not in df.columns:
        return {
            "error": f"La columna '{group_by}' no existe",
            "available_columns": list(df.columns)
        }

    # aseguramos que la columna numérica exista
    if "revenue_usd" not in df.columns:
        return {"error": "No existe la columna 'revenue_usd'"}

    df = df.groupby(group_by)["revenue_usd"].sum().reset_index()

    df = df.sort_values(by="revenue_usd", ascending=False)
    df = df.head(limit)

    df = df.fillna("")

    return df.to_dict(orient="records")