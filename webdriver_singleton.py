from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config_reader import ConfigReader


class WebDriverSingleton:
    _instance = None
    _driver = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _init_driver(self):
        browser_config = ConfigReader.get_browser_config()
        window_width = browser_config["window_width"]
        window_height = browser_config["window_height"]

        options = Options()
        options.add_argument(f"--window-size={window_width},{window_height}")

        chrome_options_config = ConfigReader.get_chrome_options()

        arguments = chrome_options_config.get("arguments", [])
        for arg in arguments:
            options.add_argument(arg)

        experimental_options = chrome_options_config.get("experimental_options", {})
        for key, value in experimental_options.items():
            options.add_experimental_option(key, value)

        service = Service(ChromeDriverManager().install())
        WebDriverSingleton._driver = webdriver.Chrome(
            service=service,
            options=options
        )

    @staticmethod
    def get_driver():
        if WebDriverSingleton._driver is None:
            WebDriverSingleton()._init_driver()
        return WebDriverSingleton._driver

    @staticmethod
    def quit():
        if WebDriverSingleton._driver:
            WebDriverSingleton._driver.quit()
            WebDriverSingleton._driver = None
            WebDriverSingleton._instance = None
