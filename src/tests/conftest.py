import pytest
from config import settings
import time
from datetime import datetime, timedelta


from utils.base_api_client import BaseApiClient
from utils.repository_api_helpers import RepositoryApiHelpers

TIMESTAMP = str(int(time.time() * 1000))


@pytest.fixture(scope="session")
def base_url():
    return settings.BASE_URL


@pytest.fixture(scope="session")
def auth_headers():
    return settings.AUTH_HEADER


@pytest.fixture
def repo_api(base_url, auth_headers):
    """Fixture that returns a RepositoryAPI client"""
    client = BaseApiClient(base_url=base_url, headers=auth_headers)
    return RepositoryApiHelpers(client)


@pytest.fixture(scope="session")
def repo_name():
    return "sid-jfrog-assignment-test-repo-" + TIMESTAMP


@pytest.fixture(scope="session")
def policy_name():
    return "auto-policy-" + TIMESTAMP


@pytest.fixture(scope="session")
def watch_name():
    return "auto-watch-" + TIMESTAMP


@pytest.fixture(scope="session")
def watch_start_date():
    return generat_timestamp(0)


@pytest.fixture(scope="session")
def watch_end_date():
    return generat_timestamp(10)


def generat_timestamp(days):
    future_time = datetime.now().astimezone() + timedelta(days=days)
    timestamp = future_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    formatted = f"{timestamp[:-2]}:{timestamp[-2:]}"
    return formatted
