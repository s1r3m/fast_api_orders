import os

APP_HOST = os.getenv('APP_HOST', 'http://localhost')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://trader:trader@localhost:5432/trader')
ORDER_EXECUTE_DELAY = os.getenv('ORDER_EXECUTE_DELAY', '1')
