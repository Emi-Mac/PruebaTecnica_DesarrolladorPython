from extract import extract
from transform import transform
#from load import load

if __name__ == "__main__":

    df = extract("dataset/data_prueba_tecnica.csv")
    print(df)
    df = transform(df)
    print(df)
    print(type(df.paid_at[0]))
    print(type(df.paid_at[3]))
    # exportar parquet
    #df.to_parquet("dataset/output.parquet", index=False)

    #load(df)
