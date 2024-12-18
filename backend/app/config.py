import os

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"

DATABASE_HOST = os.getenv('SQL_HOST')
DATABASE_NAME = os.getenv('POSTGRES_DB')
DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_PORT = os.getenv('SQL_PORT')

CLIENT_SECRET = os.getenv('CLIENT_SECRET')

STATIC_DIR: str = f'{os.path.dirname(os.path.abspath(__file__))}/static'

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
PRODUCE_TOPIC = os.getenv("WEB_TOPIC")