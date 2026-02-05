from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
import re
import time


class SearchPage(BasePage):
    VALUE_SORT_BY_LOCATOR = (By.XPATH, "//input[@id='sort_by']")
    SORT_MENU_BUTTON_LOCATOR = (By.XPATH, "//button[@id='sort_by_trigger']")
    SORT_MENU_LOCATOR = (By.XPATH, "//*[@id='sort_by_droplist']")
    SORT_PRICE_DESC_LOCATOR = (By.XPATH, "//*[@id='sort_by_droplist']//*[@id='Price_DESC']")

    SEARCH_RESULTS_LOCATOR = (By.XPATH, "//*[@id='search_resultsRows']/*")
    GAME_TITLE_LOCATOR = (By.XPATH, ".//*[@class='title']")
    GAME_BASE_PRICE_LOCATOR = (By.XPATH, ".//div[contains(@class, 'search_price_discount_combined')]")
    GAME_FINAL_PRICE_LOCATOR = (By.XPATH, ".//*[@class='discount_final_price']")

    def get_current_sort_value(self):
        return self.get_attribute(self.VALUE_SORT_BY_LOCATOR, "value")

    def open_sort_menu(self):
        if not self.is_visible(self.SORT_MENU_LOCATOR, timeout=1):
            self.click(self.SORT_MENU_BUTTON_LOCATOR)
            if not self.is_visible(self.SORT_MENU_LOCATOR):
                return False
        return True

    def close_sort_menu(self):
        if self.is_visible(self.SORT_MENU_LOCATOR, timeout=1):
            self.click(self.SORT_MENU_BUTTON_LOCATOR)
            start_time = time.time()
            while time.time() - start_time < 3:
                if not self.is_visible(self.SORT_MENU_LOCATOR, timeout=0.5):
                    return True
                time.sleep(0.1)
        return True

    def select_sort_price_desc(self):
        if not self.open_sort_menu():
            return False
        self.click(self.SORT_PRICE_DESC_LOCATOR)
        time.sleep(0.5)
        return True

    def is_sorted_by_price_desc(self):
        return "Price_DESC" == self.get_current_sort_value()

    def get_first_n_games(self, n=10):
        game_data = []
        game_elements = self.driver.find_elements(*self.SEARCH_RESULTS_LOCATOR)[:n]

        for i in range(len(game_elements)):
            try:
                current_element = self.driver.find_elements(*self.SEARCH_RESULTS_LOCATOR)
                if i >= len(current_element):
                    break

                element = current_element[i]

                game_title = self._extract_game_title(element)
                game_price = self._extract_game_price(element)

                game_data.append(
                    {"index": i,
                     "game_title": game_title,
                     "game_price": game_price})

            except StaleElementReferenceException:
                continue
            except (NoSuchElementException, IndexError):
                continue

        return game_data

    def _extract_game_data(self, game_element, index):
        return {
            'index': index,
            'game_title': self._extract_game_title(game_element),
            'game_price': self._extract_game_price(game_element)
        }

    def _extract_game_title(self, game_element):
        try:
            return game_element.find_element(*self.GAME_TITLE_LOCATOR).text.strip()
        except NoSuchElementException:
            return None

    def _extract_game_price(self, game_element):
        try:
            # Пробуем извлечь базовую цену
            price_elements = game_element.find_elements(*self.GAME_BASE_PRICE_LOCATOR)
            for price_element in price_elements:
                price_str = price_element.get_attribute("data-price-final")
                if price_str:
                    try:
                        return float(price_str)
                    except (ValueError, TypeError):
                        continue

            # Если не нашли, пробуем финальную цену
            price_elements = game_element.find_elements(*self.GAME_FINAL_PRICE_LOCATOR)
            for price_element in price_elements:
                price_text = price_element.text.strip()
                parsed = self._parse_price(price_text)
                if parsed is not None:
                    return parsed
        except NoSuchElementException:
            pass

        return None

    def _parse_price(self, text_price_element):
        if text_price_element:
            text = text_price_element.lower()
            numbers = re.findall(r'[\d,\.]+', text)
            if not numbers:
                return None
            numbers_str = numbers[-1]
            if ',' in numbers_str and '.' in numbers_str:
                if numbers_str.rfind(',') > numbers_str.rfind('.'):
                    numbers_str = numbers_str.replace('.', '').replace(',', '.')
                else:
                    numbers_str = numbers_str.replace(',', '')
            elif ',' in numbers_str:
                numbers_str = numbers_str.replace(',', '.')

            try:
                price = float(numbers_str)
                return price
            except ValueError:
                return None
        return None
