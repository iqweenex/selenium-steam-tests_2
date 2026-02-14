from enum import Enum
from selenium.webdriver.common.by import By


class Language(Enum):
    ENGLISH = "en"
    RUSSIAN = "ru"

    @property
    def locator(self) -> tuple:
        locators = {
            Language.ENGLISH: (By.XPATH, "//*[@id='language_dropdown']//a[contains(@href, 'english')]"),
            Language.RUSSIAN: (By.XPATH, "//*[@id='language_dropdown']//a[contains(@href, 'russian')]")
        }
        return locators[self]

    @property
    def button_text(self) -> str:
        texts = {
            Language.ENGLISH: "language",
            Language.RUSSIAN: "язык"
        }
        return texts[self]

    @classmethod
    def from_string(cls, value: str):
        for lang in cls:
            if lang.value == value:
                return lang
        raise ValueError(f"Неподдерживаемый язык: {value}")
