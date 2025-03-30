import csv
import os
import random
from faker import Faker

# Initialize Faker for generating fictional data in English
fake = Faker("en_US")

os.makedirs("initial_data", exist_ok=True)


# Contador para generar IDs de manera secuencial
class IDGenerator:
    def __init__(self):
        self.city_id = 1
        self.store_id = 1
        self.product_type_id = 1
        self.brand_id = 1
        self.product_id = 1
        self.product_store_id = 1

    def get_city_id(self):
        id_value = self.city_id
        self.city_id += 1
        return id_value

    def get_store_id(self):
        id_value = self.store_id
        self.store_id += 1
        return id_value

    def get_product_type_id(self):
        id_value = self.product_type_id
        self.product_type_id += 1
        return id_value

    def get_brand_id(self):
        id_value = self.brand_id
        self.brand_id += 1
        return id_value

    def get_product_id(self):
        id_value = self.product_id
        self.product_id += 1
        return id_value

    def get_product_store_id(self):
        id_value = self.product_store_id
        self.product_store_id += 1
        return id_value


# Crear instancia del generador de IDs
id_generator = IDGenerator()


# Generate city data
def generate_cities(num_cities=10):
    cities = []
    used_cities = set()
    for _ in range(num_cities):
        city_name = fake.city()
        # Ensure unique city names
        while city_name in used_cities:
            city_name = fake.city()
        used_cities.add(city_name)
        cities.append({"city_id": id_generator.get_city_id(), "name": city_name})
    return cities


# Generate store data
def generate_stores(cities, num_stores_per_city=3):
    stores = []
    for city in cities:
        for _ in range(num_stores_per_city):
            stores.append(
                {
                    "store_id": id_generator.get_store_id(),
                    "name": fake.company(),
                    "address": fake.street_address(),
                    "opening_hours": f"{random.randint(6, 20):02d}:{random.randint(0, 59):02d}:00",  # Generate random time
                    "city_id": city["city_id"],
                }
            )
    return stores


# Generate product type data
def generate_product_types():
    types = [
        "Dairy",
        "Meat",
        "Fruits",
        "Vegetables",
        "Cereals",
        "Snacks",
        "Beverages",
        "Fish",
        "Frozen Foods",
        "Bakery",
    ]
    return [
        {"product_type_id": id_generator.get_product_type_id(), "name": t}
        for t in types
    ]


# Generate brand data
def generate_brands():
    brands = [
        "Danone",
        "Nestlé",
        "Coca-Cola",
        "Pepsi",
        "Heinz",
        "Kraft",
        "Unilever",
        "Kellogg's",
        "Barilla",
        "General Mills",
    ]
    return [{"brand_id": id_generator.get_brand_id(), "name": b} for b in brands]


# Generate product data
def generate_products(brands, product_types, num_products_per_type=5):
    products = []
    for product_type in product_types:
        for _ in range(num_products_per_type):
            brand = random.choice(brands)
            products.append(
                {
                    "product_id": id_generator.get_product_id(),
                    "brand_id": brand["brand_id"],
                    "product_type_id": product_type["product_type_id"],
                    "name": f"{brand['name']} {fake.word().capitalize()} {product_type['name']}",
                    "caloric_value": random.randint(0, 100),
                    "saturated_fat_percentage": random.randint(0, 100),
                    "sugar_percentage": random.randint(0, 100),
                }
            )
    return products


# Generate price data
def generate_product_store(products, stores, num_prices_per_product=3):
    product_store = []
    for product in products:
        selected_stores = random.sample(
            stores, min(num_prices_per_product, len(stores))
        )
        for store in selected_stores:
            product_store.append(
                {
                    "product_store_id": id_generator.get_product_store_id(),
                    "product_id": product["product_id"],
                    "store_id": store["store_id"],
                    "price": round(random.uniform(0.5, 20), 2),
                    "registration_date": fake.date_between(
                        start_date="-1y", end_date="today"
                    ),
                }
            )
    return product_store


# Function to write data to CSV files
def write_to_csv(data, filename):
    if not data:
        return

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Generated {filename} with {len(data)} records")


# Main function to generate all data
def generate_initial_dataset():
    # Create directory for CSVs if it doesn't exist

    # Generate data
    cities = generate_cities()
    write_to_csv(cities, "initial_data/cities.csv")

    stores = generate_stores(cities)
    write_to_csv(stores, "initial_data/stores.csv")

    product_types = generate_product_types()
    write_to_csv(product_types, "initial_data/product_types.csv")

    brands = generate_brands()
    write_to_csv(brands, "initial_data/brands.csv")

    products = generate_products(brands, product_types)
    write_to_csv(products, "initial_data/products.csv")

    product_store = generate_product_store(products, stores)
    write_to_csv(product_store, "initial_data/product_store.csv")


# Execute data generation
if __name__ == "__main__":
    generate_initial_dataset()

# Requirements to run
# pip install faker
