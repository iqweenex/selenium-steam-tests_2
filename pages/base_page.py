from selenium.webdriver.support.ui import WebDriverWait
from webdriver_singleton import WebDriverSingleton
from config_reader import ConfigReader


class BasePage:
    def __init__(self, wait=None):
        self.driver = WebDriverSingleton.get_driver()
        browser_config = ConfigReader.get_browser_config()
        default_timeout = browser_config["timeout"]
        self.wait = wait or WebDriverWait(self.driver, default_timeout)

    def find_element_in_element(self, parent_element, locator, timeout=None):
        timeout = timeout or ConfigReader.get_browser_config()['timeout']
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(
            lambda d: parent_element.find_element(*locator)
        )

    def find_elements_in_element(self, parent_element, locator, timeout=None):
        timeout = timeout or ConfigReader.get_browser_config()['timeout']
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(
            lambda d: parent_element.find_elements(*locator)
        )
