from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config_reader import ConfigReader


class SearchPage(BasePage):
    VALUE_SORT_BY_LOCATOR = (By.ID, "sort_by")
    SORT_MENU_BUTTON_LOCATOR = (By.ID, "sort_by_trigger")
    SORT_MENU_LOCATOR = (By.ID, "sort_by_droplist")
    SORT_PRICE_DESC_LOCATOR = (By.XPATH, "//*[@id='sort_by_droplist']//*[@id='Price_DESC']")

    SEARCH_RESULTS_LOCATOR = (By.XPATH, "//*[@id='search_resultsRows']/*")
    GAME_TITLE_LOCATOR = (By.XPATH, ".//*[@class='title']")
    GAME_BASE_PRICE_LOCATOR = (By.XPATH, ".//div[contains(@class, 'search_price_discount_combined ')]")
    GAME_FINAL_PRICE_LOCATOR = (By.XPATH, ".//div[contains(@class, 'discount_block')]")

    SEARCH_RESULTS_READY_LOCATOR = (By.ID, "search_results_loading")
    SEARCH_LOADING_ELEMENT_LOCATOR = (By.XPATH, "//*[@id='search_result_container' and contains(@style,'opacity')]")

    def select_sort_price_desc(self):
        browser_config = ConfigReader.get_browser_config()
        timeout = browser_config['timeout']  # получили timeout из конфига

        # жмем на меню сортировки и ждем выпадающего списка
        self.wait.until(EC.element_to_be_clickable(self.SORT_MENU_BUTTON_LOCATOR)).click()
        self.wait.until(EC.visibility_of_element_located(self.SORT_MENU_LOCATOR))
        # выбираем сортировку по убыванию цены
        self.wait.until(EC.element_to_be_clickable(self.SORT_PRICE_DESC_LOCATOR)).click()
        # ждем загрузки
        WebDriverWait(self.driver, timeout=timeout, poll_frequency=0.05).until(
            EC.visibility_of_element_located(self.SEARCH_LOADING_ELEMENT_LOCATOR)
        )
        WebDriverWait(self.driver, timeout=timeout, poll_frequency=0.05).until(
            EC.invisibility_of_element_located(self.SEARCH_LOADING_ELEMENT_LOCATOR)
        )

    def get_first_n_games(self, n=10):
        game_data = []

        game_elements = self.wait.until(
            EC.visibility_of_all_elements_located(self.SEARCH_RESULTS_LOCATOR)
        )[:n]

        for i, element in enumerate(game_elements):
            game_title = self._extract_game_title(element)
            game_price = self._extract_game_price(element)

            game_data.append({
                "index": i,
                "game_title": game_title,
                "game_price": game_price
            })

        return game_data

    def _extract_game_data(self, game_element, index):
        return {
            'index': index,
            'game_title': self._extract_game_title(game_element),
            'game_price': self._extract_game_price(game_element)
        }

    def _extract_game_title(self, game_element):
        title_element = self.find_element_in_element(game_element, self.GAME_TITLE_LOCATOR)
        return title_element.text.strip()

    def _extract_game_price(self, game_element):
        price_element_base = self.find_element_in_element(game_element, self.GAME_BASE_PRICE_LOCATOR)
        price_element_final = self.find_element_in_element(game_element, self.GAME_FINAL_PRICE_LOCATOR)

        price_str_base = price_element_base.get_attribute("data-price-final")
        price_str_final = price_element_final.get_attribute("data-price-final")

        price = max(self._parse_price(price_str_final), self._parse_price(price_str_base))
        if price is None:
            return 0.0
        return price

    def _parse_price(self, price_str):
        if price_str is None:
            return 0.0
        return float(price_str)
