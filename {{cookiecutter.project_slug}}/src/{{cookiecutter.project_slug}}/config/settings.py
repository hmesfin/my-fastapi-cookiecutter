import os
from functools import lru_cache

from {{ cookiecutter.project_slug }}.config.base import BaseAppSettings


@lru_cache
def get_settings() -> BaseAppSettings:
  env = os.getenv("FASTAPI_ENV", "local")
  settings_map = {
    "local": "{{ cookiecutter.project_slug }}.config.local.LocalSettings",
    "production": "{{ cookiecutter.project_slug }}.config.production.ProductionSettings",
    "test": "{{ cookiecutter.project_slug }}.config.test.TestSettings",
  }
  module_path, class_name = settings_map[env].rsplit(".", 1)
  import importlib
  module = importlib.import_module(module_path)
  settings_class = getattr(module, class_name)
  return settings_class()
