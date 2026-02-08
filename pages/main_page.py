from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.search_page import SearchPage
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BasePage):
    SEARCH_FIELD_LOCATOR = (By.XPATH, "//form[@role='search']//input[@type='text']")
    SEARCH_BUTTON_LOCATOR = (By.XPATH, "//form[@role='search']//button[@type='submit']")
    def open_steam_main_page(self):
        return self.driver.get("https://store.steampowered.com/")

    def search_game(self, game_name):
        self.type_text(self.SEARCH_FIELD_LOCATOR, game_name)
        self.click(self.SEARCH_BUTTON_LOCATOR)

        search_page = SearchPage(self.wait)
        search_page.wait.until(EC.presence_of_element_located(SearchPage.SEARCH_RESULTS_LOCATOR))
        return search_page
