CREATE TABLE companies (
    id VARCHAR(40) PRIMARY KEY,
    company_name VARCHAR(130)
);

CREATE TABLE charges (
    id VARCHAR(40) PRIMARY KEY,
    company_id VARCHAR(40) REFERENCES companies(id),  /*Aqui estamos haciendo coincidir con el id de la tabla companies
    una sola empresa puede tener muchas transacciones, pero cada transaccion le pertenece a una sola empresa*/
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    paid_at TIMESTAMP
);
