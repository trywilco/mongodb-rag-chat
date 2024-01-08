import asyncpg
from fastapi import FastAPI
from loguru import logger

from app1.core.settings.app1 import AppSettings


async def connect_to_db(app1: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    # SQLAlchemy >= 1.4 deprecated the use of `postgres://` in favor of `postgresql://`
    # for the database connection url
    database_url = settings.database_url.replace("postgres://", "postgresql://")

    app1.state.pool = await asyncpg.create_pool(
        str(database_url),
        min_size=settings.min_connection_count,
        max_size=settings.max_connection_count,
    )

    logger.info("Connection established")


async def close_db_connection(app1: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app1.state.pool.close()

    logger.info("Connection closed")
