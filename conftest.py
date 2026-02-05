import pytest
import time

from selenium.webdriver.support.ui import WebDriverWait
from webdriver_singleton import WebDriverSingleton

TIMEOUT = 10

@pytest.fixture(scope="session")
def driver():
    driver = WebDriverSingleton.get_driver()
    yield driver

@pytest.fixture()
def wait(driver):
    return WebDriverWait(driver, TIMEOUT)

@pytest.fixture(autouse=True)
def clean_between_tests(driver):
    driver.delete_all_cookies()
    yield
    driver.get("about:blank")
    time.sleep(0.5)

@pytest.fixture(scope="session", autouse=True)
def driver_teardown():
    yield
    WebDriverSingleton.quit_driver()
