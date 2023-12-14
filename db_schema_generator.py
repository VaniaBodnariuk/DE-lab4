import os
from pathlib import Path

def create_db_if_absent(connection, config):
    db_name = config.get("database")
    db_owner = config.get("user")

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"""
                CREATE DATABASE {db_name}
                    WITH
                    OWNER = {db_owner}
                    ENCODING = 'UTF8'
                    CONNECTION LIMIT = -1
                    IS_TEMPLATE = False;
                           """)

def create_table_if_absent(table_name: str, connection):
    ddl_path = f"ddl/{table_name}.sql"
    ddl_script = Path(ddl_path).read_text()
    with connection.cursor() as cursor:
        cursor.execute(ddl_script)
    connection.commit()
    cursor.close()
