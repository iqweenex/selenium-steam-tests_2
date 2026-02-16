from selenium.webdriver.support.ui import WebDriverWait
from utils.webdriver_singleton import WebDriverSingleton
from utils.config_reader import ConfigReader


class BasePage:
    def __init__(self, wait=None):
        self.driver = WebDriverSingleton.get_driver()
        browser_config = ConfigReader.get_browser_config()
        default_timeout = browser_config["timeout"]
        self.wait = wait or WebDriverWait(self.driver, default_timeout)