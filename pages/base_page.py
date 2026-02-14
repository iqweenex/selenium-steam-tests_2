from selenium.webdriver.support.ui import WebDriverWait
from webdriver_singleton import WebDriverSingleton
from config_reader import ConfigReader


class BasePage:
    def __init__(self, wait=None):
        self.driver = WebDriverSingleton.get_driver()
        browser_config = ConfigReader.get_browser_config()
        default_timeout = browser_config["timeout"]
        self.wait = wait or WebDriverWait(self.driver, default_timeout)