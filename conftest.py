import atexit
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_singleton import WebDriverSingleton
from config_reader import ConfigReader


@pytest.fixture(scope="function")
def driver():
    driver = WebDriverSingleton.get_driver()

    def cleanup():
        WebDriverSingleton.quit()

    atexit.register(cleanup)
    yield driver
    WebDriverSingleton.quit()


@pytest.fixture()
def wait(driver):
    browser_config = ConfigReader.get_browser_config()
    timeout = browser_config["timeout"]
    return WebDriverWait(driver, timeout)


@pytest.fixture()
def clean_page(driver):
    url = ConfigReader.get_urls()["steam_main_page"]
    driver.get(url)
    driver.delete_all_cookies()
    yield driver
