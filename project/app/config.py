import os
from urllib.parse import urlparse


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/locker_dev"
)

parsed_url = urlparse(DATABASE_URL)

DB_CONFIG = {
    "dbname": parsed_url.path.lstrip("/"),
    "user": parsed_url.username,
    "password": parsed_url.password,
    "host": parsed_url.hostname,
    "port": parsed_url.port,
}
