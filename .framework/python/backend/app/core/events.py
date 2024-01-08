from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app1.core.settings.app1 import AppSettings
from app1.db.events import close_db_connection, connect_to_db


def create_start_app_handler(
    app1: FastAPI,
    settings: AppSettings,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_db(app1, settings)

    return start_app


def create_stop_app_handler(app1: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        await close_db_connection(app1)

    return stop_app
