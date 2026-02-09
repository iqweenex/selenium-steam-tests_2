from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.search_page import SearchPage
from selenium.webdriver.support import expected_conditions as EC
from config_reader import config


class MainPage(BasePage):
    SEARCH_FIELD_LOCATOR = (By.XPATH, "//form[@role='search']//input[@type='text']")
    SEARCH_BUTTON_LOCATOR = (By.XPATH, "//form[@role='search']//button[@type='submit']")

    def open_steam_main_page(self, language='en'):
        if language == 'ru':
            return self.driver.get(config.get("urls.steam_main_page_ru"))
        return self.driver.get(config.get("urls.steam_main_page_en"))

    def search_game(self, game_name):
        element = self.wait.until(EC.visibility_of_element_located(self.SEARCH_FIELD_LOCATOR))
        element.clear()
        element.send_keys(game_name)

        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON_LOCATOR)).click()

        search_page = SearchPage(self.wait)
        search_page.wait.until(EC.presence_of_element_located(SearchPage.SEARCH_RESULTS_LOCATOR))
        return search_page
