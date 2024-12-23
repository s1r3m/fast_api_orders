import os

HOST = os.getenv('HOST', 'localhost')
APP_HOST = f'http://{HOST}'
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://trader:trader@localhost:5432/trader')
