from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config_reader import ConfigReader


class WebDriverSingleton:
    _driver = None

    def __new__(cls):
        if cls._driver is None:
            cls._driver = cls._create_driver()
        return cls._driver

    @staticmethod
    def _create_driver():
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
        return webdriver.Chrome(
            service=service,
            options=options
        )

    @staticmethod
    def get_driver():
        return WebDriverSingleton()

    @staticmethod
    def quit():
        if WebDriverSingleton._driver:
            WebDriverSingleton._driver.quit()
            WebDriverSingleton._driver = None
