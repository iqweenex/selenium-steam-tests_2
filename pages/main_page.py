from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from utils.config_reader import ConfigReader
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from enums.language import Language


class MainPage(BasePage):
    SEARCH_FIELD_LOCATOR = (By.XPATH, "//form[@role='search']//input[@type='text']")
    SEARCH_BUTTON_LOCATOR = (By.XPATH, "//form[@role='search']//button[@type='submit']")
    LANGUAGE_PULLDOWN_LOCATOR = (By.ID, "language_pulldown")
    LANGUAGE_DROPDOWN_LOCATOR = (By.ID, "language_dropdown")

    LOADING_LANGUAGE_LOCATOR = (By.XPATH, "//*[@class='waiting_dialog_throbber']")

    _EXPECTED_BUTTON_TEXTS = {
        Language.ENGLISH: "language",
        Language.RUSSIAN: "язык"
    }

    _LANGUAGE_LOCATORS = {
        Language.ENGLISH: (By.XPATH, "//*[@id='language_dropdown']//a[contains(@href, 'english')]"),
        Language.RUSSIAN: (By.XPATH, "//*[@id='language_dropdown']//a[contains(@href, 'russian')]")
    }

    def change_language(self, language: Language):
        timeout = ConfigReader.get_browser_config()['timeout']
        current_button_text = self.wait.until(
            EC.element_to_be_clickable(self.LANGUAGE_PULLDOWN_LOCATOR)).text.lower()

        if current_button_text != self._EXPECTED_BUTTON_TEXTS[language]:
            self.wait.until(EC.element_to_be_clickable(self.LANGUAGE_PULLDOWN_LOCATOR)).click()
            self.wait.until(EC.visibility_of_element_located(self.LANGUAGE_DROPDOWN_LOCATOR))

            self.wait.until(EC.element_to_be_clickable(self._LANGUAGE_LOCATORS[language])).click()
            WebDriverWait(self.driver, timeout=timeout, poll_frequency=0.1).until(
                EC.presence_of_element_located(self.LOADING_LANGUAGE_LOCATOR)
            )
            WebDriverWait(self.driver, timeout=timeout, poll_frequency=0.1).until_not(
                EC.presence_of_element_located(self.LOADING_LANGUAGE_LOCATOR)
            )

            self.wait.until(EC.presence_of_element_located(self.SEARCH_FIELD_LOCATOR))

    def search_game(self, game_name):
        self.wait.until(EC.visibility_of_element_located(self.SEARCH_FIELD_LOCATOR)).clear()
        element = self.wait.until(EC.visibility_of_element_located(self.SEARCH_FIELD_LOCATOR))
        element.send_keys(game_name)
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON_LOCATOR)).click()
