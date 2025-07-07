"""Test level fixture file"""

import time
import pytest
import allure
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.constants import EnvironmentParams
from config.constants import ApiTestConfs

from utils.base_api_client import BaseApiClient
from utils.api_helpers import JfrogApiHelpers

# creating uniq timestamp to use in all resource creation
TIMESTAMP = str(int(time.time() * 1000))


@pytest.fixture(scope="session")
def base_url():
    """base_url fixture"""
    return EnvironmentParams.BASE_URL


@pytest.fixture(scope="session")
def auth_headers():
    """auth header fixture"""
    return EnvironmentParams.AUTH_HEADER


@pytest.fixture
def repo_api(base_url, auth_headers):
    """Fixture that returns a RepositoryAPI client"""
    client = BaseApiClient(base_url=base_url, headers=auth_headers)
    return JfrogApiHelpers(client)


@pytest.fixture(scope="session")
def repo_name():
    """repo name fixture"""
    return ApiTestConfs.REPO_PREFIX + TIMESTAMP


@pytest.fixture(scope="session")
def policy_name():
    """policy name fixture"""
    return ApiTestConfs.POLICY_PREFIX + TIMESTAMP


@pytest.fixture(scope="session")
def watch_name():
    """watch name fixture"""
    return ApiTestConfs.WATCH_PREFIX + TIMESTAMP


@pytest.fixture(scope="session")
def watch_start_date():
    """watch start date fixture"""
    return generat_timestamp(0)


@pytest.fixture(scope="session")
def watch_end_date():
    """watch end date fixture"""
    return generat_timestamp(10)


def generat_timestamp(days):
    """function to generate the UTC time in RFC3339"""
    future_time = datetime.now().astimezone() + timedelta(days=days)
    timestamp = future_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    formatted = f"{timestamp[:-2]}:{timestamp[-2:]}"
    return formatted


@pytest.fixture(scope="function")
def driver():
    """webdriver fixture for UI testcases"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
