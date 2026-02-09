import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_singleton import WebDriverSingleton
from config_reader import config


# отдельный config.json и класс по его управлению

@pytest.fixture(scope="function")
def driver():
    webdriver_instance = WebDriverSingleton()
    driver = webdriver_instance.get_driver()
    yield driver
    webdriver_instance.quit()

@pytest.fixture()
def wait(driver):
    browser_config = config.get_browser_config()
    timeout = browser_config["timeout"]
    return WebDriverWait(driver, timeout)
