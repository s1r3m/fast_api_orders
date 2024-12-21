from logging.config import fileConfig

from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine

from trader.settings import DATABASE_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from trader.db import Base

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
# Define the asynchronous database engine configuration

def get_engine():
    return async_engine_from_config(
        {
            "sqlalchemy.url": DATABASE_URL,
        },
        poolclass=pool.NullPool,
    )

async def run_migrations_online():
    """
    Run migrations in 'online' mode using an async connection.
    """
    connectable = get_engine()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    """
    Define and execute migrations for the connection.
    """
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

# Run migrations
from asyncio import run
run(run_migrations_online())
