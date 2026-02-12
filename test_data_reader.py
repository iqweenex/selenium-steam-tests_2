import json
import os
from typing import Any, Dict, List


class TestDataReader:
    TEST_DATA_PATH = "test_data.json"
    _test_data = None

    @classmethod
    def load_test_data(cls, test_data_path: str = None) -> Dict[str, Any]:
        if cls._test_data is None:
            path = test_data_path or cls.TEST_DATA_PATH
            if not os.path.exists(path):
                raise FileNotFoundError(f"Файл не найден: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                cls._test_data = json.load(f)
        return cls._test_data

    @classmethod
    def get(cls, key_path: str, default: Any = None) -> Any:
        test_data = cls.load_test_data()

        keys = key_path.split('.')
        value = test_data

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    @classmethod
    def get_games(cls) -> List[Dict[str, Any]]:
        return cls.get("games", [])
