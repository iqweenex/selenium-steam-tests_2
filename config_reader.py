import json
import os
from typing import Any, Dict


class ConfigReader:
    _config = None

    @classmethod
    def load_config(cls, config_path: str = "config.json") -> Dict[str, Any]:
        if cls._config is None:
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Файл конфига не найден: {config_path}")
            with open(config_path, 'r', encoding='utf-8') as f:
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
    def get_urls(cls) -> Dict[str, str]:
        return cls.get("urls", {})

    @classmethod
    def get_test_data(cls) -> Dict[str, Any]:
        return cls.get("test_data", {})

config = ConfigReader()

if __name__ == "__main__":
    print("=== Тестируем ConfigReader ===")
    print(f"Ширина окна: {config.get('browser.window_width')}")
    print(f"Высота окна: {config.get('browser.window_height')}")  # ← ПРАВИЛЬНО!
    print(f"Таймаут: {config.get('browser.timeout')}")
    print(f"URL Steam: {config.get('urls.steam_main_page')}")  # ← ПРАВИЛЬНО!
    print(f"URL Steam RU: {config.get('urls.steam_main_page_ru')}")
    print(f"URL Steam EN: {config.get('urls.steam_main_page_en')}")
    print(f"Игры: {config.get('test_data.games')}")
