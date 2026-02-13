from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from config_reader import ConfigReader
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):
    SEARCH_FIELD_LOCATOR = (By.XPATH, "//form[@role='search']//input[@type='text']")
    SEARCH_BUTTON_LOCATOR = (By.XPATH, "//form[@role='search']//button[@type='submit']")
    LANGUAGE_PULLDOWN_LOCATOR = (By.ID, "language_pulldown")
    LANGUAGE_DROPDOWN_LOCATOR = (By.ID, "language_dropdown")

    ENGLISH_LANG_LOCATOR = (By.XPATH, "//*[@id='language_dropdown']//a[contains(@href, 'english')]")
    RUSSIAN_LANG_LOCATOR = (By.XPATH, "//*[@id='language_dropdown']//a[contains(@href, 'russian')]")

    LOADING_LANGUAGE_LOCATOR = (By.XPATH, "//*[@class='waiting_dialog_throbber']")

    def change_language(self, language):
        timeout = ConfigReader.get_browser_config()['timeout']
        current_language = self.wait.until(
            EC.element_to_be_clickable(self.LANGUAGE_PULLDOWN_LOCATOR)).text.lower()

        need_change = False
        if language == 'en' and current_language != 'language':
            lang_locator = self.ENGLISH_LANG_LOCATOR
            need_change = True
        if language == 'ru' and current_language != 'язык':
            lang_locator = self.RUSSIAN_LANG_LOCATOR
            need_change = True

        if need_change:
            self.wait.until(EC.element_to_be_clickable(self.LANGUAGE_PULLDOWN_LOCATOR)).click()
            self.wait.until(EC.element_to_be_clickable(lang_locator)).click()
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
