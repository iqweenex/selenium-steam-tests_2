from enum import Enum


class Language(Enum):
    ENGLISH = "en"
    RUSSIAN = "ru"

    @classmethod
    def from_string(cls, value: str):
        for lang in cls:
            if lang.value == value:
                return lang
        raise ValueError(f"Неподдерживаемый язык: {value}")
