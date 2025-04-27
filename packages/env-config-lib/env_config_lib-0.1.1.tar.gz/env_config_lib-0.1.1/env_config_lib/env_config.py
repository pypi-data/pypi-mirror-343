# env_config.py



import os
import ast
from typing import Dict, Any, Optional, Type

from dotenv import load_dotenv

class EnvConfigError(Exception):
    """Ошибка конфигурации окружения"""
    pass



class EnvConfig:
    def __init__(self, schema: Dict[str, Type], path: str = ".env"):
        load_dotenv(path)
        self._schema = schema
        self._config: Dict[str, Any] = {}

        for key, expected_type in schema.items():
            raw_value = os.getenv(key)
            if raw_value is None:
                raise EnvConfigError(f"Отсутствует переменная окружения: {key}")

            try:
                parsed_value = ast.literal_eval(raw_value)
            except (ValueError, SyntaxError):
                parsed_value = raw_value

            try:
                final_value = expected_type(parsed_value)
            except (ValueError, TypeError):
                raise EnvConfigError(f"Ошибка преобразования переменной {key} в тип {expected_type.__name__}.")

            self._config[key] = final_value

    def get_config(self) -> Dict[str, Any]:
        """Получить все переменные окружения в виде словаря"""

        return self._config

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Получить значение переменной окружения по ключу"""

        
        if key in self._config:
            return self._config[key]
        if default is not None:
            return default
        raise EnvConfigError(f"Переменная {key} не найдена и значение по умолчанию не указано.")

    def get_schema(self) -> Dict[str, Type]:
        """Получить схему переменных окружения"""

        return self._schema
