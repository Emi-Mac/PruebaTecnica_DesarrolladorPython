from extract import extract
from transform import transform
from load import load

if __name__ == "__main__":

    df = extract("dataset/data_prueba_tecnica.csv")
    df = transform(df)

    # exportar parquet
    df.to_parquet("dataset/output.parquet", index=False)

    load(df)
