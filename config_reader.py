import json
import os
from typing import Any, Dict


class ConfigReader:
    CONFIG_PATH = "config.json"
    _config = None

    @classmethod
    def load_config(cls, config_path: str = CONFIG_PATH) -> Dict[str, Any]:
        if cls._config is None:
            path = config_path or cls.CONFIG_PATH
            if not os.path.exists(path):
                raise FileNotFoundError(f"Файл конфига не найден: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                cls._config = json.load(f)

        return cls._config

    @classmethod
    def get(cls, key_path: str, default: Any = None) -> Any:
        config = cls.load_config()

        keys = key_path.split('.')
        value = config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    @classmethod
    def get_browser_config(cls) -> Dict[str, Any]:
        return cls.get("browser", {})

    @classmethod
    def get_chrome_options(cls) -> Dict[str, Any]:
        return cls.get("chrome_options", {})

    @classmethod
    def get_urls(cls) -> Dict[str, str]:
        return cls.get("urls", {})
