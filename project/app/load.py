import csv
import os
import psycopg2


path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "scripts",
    "initial_data",
)


def load_csv_to_table(csv_file, table_name, columns, db_config):
    full_path = os.path.join(path, csv_file)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")

    with open(full_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = [tuple(row[col] for col in columns) for row in reader]

    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            placeholders = ", ".join(["%s"] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cur.executemany(query, rows)

            sync_query = f"SELECT setval('public.{table_name}_{table_name}_id_seq', (SELECT MAX({table_name}_id) FROM public.{table_name}), true)"
            cur.execute(sync_query)

        conn.commit()


def load_data(db_config):
    load_csv_to_table("cities.csv", "city", ["city_id", "name"], db_config)
    load_csv_to_table(
        "stores.csv",
        "store",
        ["store_id", "name", "address", "opening_hours", "city_id"],
        db_config,
    )
    load_csv_to_table(
        "product_types.csv",
        "product_type",
        ["product_type_id", "name"],
        db_config,
    )
    load_csv_to_table("brands.csv", "brand", ["brand_id", "name"], db_config)

    load_csv_to_table(
        "products.csv",
        "product",
        [
            "product_id",
            "brand_id",
            "product_type_id",
            "name",
            "caloric_value",
            "saturated_fat_percentage",
            "sugar_percentage",
        ],
        db_config,
    )

    load_csv_to_table(
        "product_store.csv",
        "product_store",
        [
            "product_store_id",
            "product_id",
            "store_id",
            "price",
            "registration_date",
        ],
        db_config,
    )
