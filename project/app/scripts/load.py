import csv
import argparse
import os
import psycopg2


path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "project",
    "app",
    "scripts",
    "initial_data",
)


def load_csv_to_table(csv_file, table_name, columns, db_config):
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = [tuple(row[col] for col in columns) for row in reader]

    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            placeholders = ", ".join(["%s"] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cur.executemany(query, rows)
            conn.commit()


def load_data(db_config):
    load_csv_to_table("/cities.csv", "city", ["city_id", "name"], db_config)

    load_csv_to_table(
        path + "/stores.csv",
        "store",
        ["store_id", "name", "/address", "opening_hours", "city_id"],
        db_config,
    )

    load_csv_to_table(
        path + "/product_types.csv",
        "product_type",
        ["product_type_id", "name"],
        db_config,
    )

    load_csv_to_table(path + "/brands.csv", "brand", ["brand_id", "name"], db_config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load CSV data into the database.")
    parser.add_argument("--dbname", required=True, help="Database name")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--port", required=True, type=int, help="Database port")

    args = parser.parse_args()

    db_config = {
        "dbname": args.dbname,
        "user": args.user,
        "password": args.password,
        "host": args.host,
        "port": args.port,
    }

    load_data(db_config)
