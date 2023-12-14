from psycopg2 import sql
import csv
import os

def load_csv_data_to_table(table_name: str, connection):
    data_path = f"data/{table_name}.csv"

    with connection.cursor() as cursor:
        with open(data_path, 'r', encoding='utf-8') as csv_file:
            clean_up_table(cursor, table_name)
            populate_table(csv.reader(csv_file), cursor, table_name)

    connection.commit()
    cursor.close()


def clean_up_table(cursor, table_name):
    cursor.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(table_name)))


def populate_table(csv_reader, cursor, table_name):
    header = next(csv_reader)
    data = [[value.strip() for value in row] for row in csv_reader]
    inserts = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(map(lambda col: sql.Identifier(col.strip()), header)),
        sql.SQL(", ").join(sql.Placeholder() * len(header)),
    )
    cursor.executemany(inserts, data)
