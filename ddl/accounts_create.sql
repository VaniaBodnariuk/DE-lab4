-- The SQL script is generated for accounts.csv by ddl_scripts_generator.py
CREATE TABLE IF NOT EXISTS accounts (
    customer_id INTEGER,
     first_name TEXT,
     last_name TEXT,
     address_1 TEXT,
     address_2 TEXT,
     city TEXT,
     state TEXT,
     zip_code INTEGER,
     join_date DATE,
    PRIMARY KEY (customer_id));
