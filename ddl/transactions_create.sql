-- The SQL script is generated for transactions.csv by ddl_scripts_generator.py
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT,
     transaction_date DATE,
     product_id INTEGER,
     product_code INTEGER,
     product_description TEXT,
     quantity INTEGER,
     account_id INTEGER,
    PRIMARY KEY (transaction_id));
ALTER TABLE transactions ADD FOREIGN KEY IF NOT EXISTS (product_id) REFERENCES products(product_id);
CREATE INDEX IF NOT EXISTS transactions_product_id_idx ON transactions(product_id);
ALTER TABLE transactions ADD FOREIGN KEY IF NOT EXISTS (account_id) REFERENCES accounts(customer_id);
CREATE INDEX IF NOT EXISTS transactions_customer_id_idx ON transactions(customer_id);
