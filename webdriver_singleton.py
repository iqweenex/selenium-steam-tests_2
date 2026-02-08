from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

class WebDriverSingleton:
    _driver = None

    @classmethod
    def get_driver(cls, window_size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
        if cls._driver is None:
            options = Options()
            options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            service = Service(ChromeDriverManager().install())

            cls._driver = webdriver.Chrome(
                service=service,
                options=options
            )
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None