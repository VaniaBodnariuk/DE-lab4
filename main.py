import glob
import os

import psycopg2

from ddl_scripts_generator import generate_ddl_files_from_csv
from db_schema_generator import create_table_if_absent, create_db_if_absent
from csv_to_db_data_loader import load_csv_data_to_table

BASE_DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

LAB_DB_CONFIG = {
    'host': 'localhost',
    'database': 'de_lab4',
    'user': 'postgres',
    'password': 'postgres'
}

def main():
    csv_files = scan_csv_files()
    generate_ddl_files_from_csv(csv_files)
    # generate_populated_db(csv_files)

def scan_csv_files():
    csv_files = glob.glob(f'data/*.csv', recursive=True)
    return csv_files
def generate_populated_db(csv_files):
    connection = get_db_connection()
    for file_path in csv_files:
        generate_populated_table(connection, table_name=os.path.splitext(os.path.basename(file_path))[0])
    connection.close()

def generate_populated_table(connection, table_name):
    create_table_if_absent(table_name, connection)
    load_csv_data_to_table(table_name, connection)

def get_db_connection():
    in_conn = psycopg2.connect(**BASE_DB_CONFIG)
    create_db_if_absent(in_conn, LAB_DB_CONFIG)
    connection = psycopg2.connect(**LAB_DB_CONFIG)
    return connection

if __name__ == "__main__":
    main()
