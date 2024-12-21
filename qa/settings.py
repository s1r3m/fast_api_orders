import os

APP_HOST = os.getenv('APP_HOST', 'http://localhost')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://trader:trader@localhost:5432/trader')
