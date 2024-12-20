import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://trader:trader@localhost:5432/trader')
ORDER_EXECUTE_DELAY = os.getenv('ORDER_EXECUTE_DELAY', 10)
