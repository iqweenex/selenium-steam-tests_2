from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_singleton import WebDriverSingleton
from config_reader import config

#удалить все методы отвечающие за действие над ЭЛЕМЕНТОМ


class BasePage:
    def __init__(self, wait=None):
        webdriver_instance = WebDriverSingleton()
        self.driver = webdriver_instance.get_driver()

        browser_config = config.get_browser_config()
        default_timeout = browser_config["timeout"]

        self.wait = wait or WebDriverWait(self.driver, default_timeout)

    def get_attribute(self, locator, attr_name):
        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )
        return element.get_attribute(attr_name)
