from sqlalchemy import create_engine  #Vamos a usar sqlalchemy para poder comunicarnos con la base de datos

def load(df):

    engine = create_engine(
        "postgresql://admin:admin@db:5432/charges_db"   #Creamos el engine que hará la comunicación
    )

    with engine.begin() as connection:  #Ahora, esta parte se cambió para realizar updates y poder ejecutar 
        #varias veces el pipeline con el mismo archivo csv sin que nos arroje un error y se detenga. Antes estaba con
        #to_sql(if_exists='append')

        # UPSERT companies
        for _, row in df[['company_id', 'name']].drop_duplicates().iterrows():
            connection.execute(text("""
                INSERT INTO companies (id, company_name)
                VALUES (:id, :company_name)
                ON CONFLICT (id)
                DO UPDATE SET company_name = EXCLUDED.company_name;
            """), {
                "id": row['company_id'],
                "company_name": row['name']
            })

        # UPSERT charges
        for _, row in df.iterrows():
            connection.execute(text("""
                INSERT INTO charges (id, company_id, amount, status, created_at, paid_at)
                VALUES (:id, :company_id, :amount, :status, :created_at, :paid_at)
                ON CONFLICT (id)
                DO UPDATE SET
                    amount = EXCLUDED.amount,
                    status = EXCLUDED.status,
                    paid_at = EXCLUDED.paid_at;
            """), {
                "id": row['id'],
                "company_id": row['company_id'],
                "amount": row['amount'],
                "status": row['status'],
                "created_at": row['created_at'],
                "paid_at": row['paid_at']
            })

    print("Datos cargados con UPSERT correctamente")
