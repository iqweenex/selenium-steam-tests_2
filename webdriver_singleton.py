from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config_reader import config


# сделать через __new__

class WebDriverSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebDriverSingleton, cls).__new__(cls)
            browser_config = config.get_browser_config()
            window_width = browser_config["window_width"]
            window_height = browser_config["window_height"]

            options = Options()
            options.add_argument(f"--window-size={window_width},{window_height}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            service = Service(ChromeDriverManager().install())

            cls._instance.driver = webdriver.Chrome(
                service=service,
                options=options
            )
        return cls._instance

    def get_driver(self):
        return self.driver

    def quit(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
        WebDriverSingleton._instance = None

    @classmethod
    def create_driver(cls):
        return cls()

    @classmethod
    def quit_driver(cls):
        if cls._instance:
            cls._instance.quit()
