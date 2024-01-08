from functools import lru_cache
from typing import Dict, Type

from app1.core.settings.app1 import AppSettings
from app1.core.settings.base import AppEnvTypes, BaseAppSettings
from app1.core.settings.development import DevAppSettings
from app1.core.settings.production import ProdAppSettings
from app1.core.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
