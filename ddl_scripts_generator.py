import csv
import os
from _pydatetime import datetime


def generate_ddl_files_from_csv(csv_files):
    for file_path in csv_files:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            table_name = os.path.splitext(os.path.basename(file_path))[0]
            create_script = __generate_table_create_script(reader, table_name)
            if not os.path.exists("ddl"):
                os.makedirs("ddl")
            with open(f"ddl/{table_name}_create.sql", 'w') as sqlfile:
                sqlfile.write(create_script)


def __generate_table_create_script(reader, table_name):
    sample_row = next(reader)
    columns = {column: __determine_data_type(sample_row[column]) for column in sample_row}
    create_script = __generate_basic_table_create_script(table_name, columns)
    if table_name == "transactions":
        create_script += __generate_indexed_foreign_key_script(table_name, "product_id", "products", "product_id")
        create_script += __generate_indexed_foreign_key_script(table_name, "account_id", "accounts", "customer_id")
    return create_script


def __generate_basic_table_create_script(table_name, columns):
    script = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    for column_name, data_type in columns.items():
        script += f"    {column_name} {data_type},\n"
    script = script.rstrip(',\n') + f",\n    PRIMARY KEY ({list(columns.keys())[0]}));\n"
    return script


def __generate_foreign_key_script(table_name, foreign_key, reference_table, reference_column):
    return f"ALTER TABLE {table_name} ADD FOREIGN KEY IF NOT EXISTS ({foreign_key}) REFERENCES {reference_table}({reference_column});\n"


def __generate_indexed_foreign_key_script(table_name, foreign_key, reference_table, reference_column):
    return (__generate_foreign_key_script(table_name, foreign_key, reference_table, reference_column)
            + __generate_index_script(table_name, reference_column))


def __generate_index_script(table_name, index_column, is_unique=False):
    unique_str = "UNIQUE " if is_unique else ""
    index_name = f"{table_name.lower()}_{index_column.lower()}_idx"
    return f"CREATE {unique_str}INDEX IF NOT EXISTS {index_name} ON {table_name}({index_column});\n"


def __determine_data_type(value):
    value_without_spaces = value.replace(" ", "")

    if value_without_spaces.isdigit():
        return "INTEGER"

    if __is_date(value_without_spaces):
        return "DATE"

    return "TEXT"


def __is_date(value):
    try:
        datetime.strptime(value, '%Y/%m/%d')
        return True
    except ValueError:
        return False
