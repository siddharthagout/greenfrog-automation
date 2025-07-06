import pytest
from config import settings
import time

from utils.base_api_client import BaseApiClient
from utils.repository_api_helpers import RepositoryApiHelpers




@pytest.fixture(scope="session")
def base_url():
    return settings.BASE_URL

@pytest.fixture(scope="session")
def auth_headers():
    return settings.AUTH_HEADER

@pytest.fixture(scope="session")
def repo_name():
    return "sid-" + str(int(time.time()*1000))

@pytest.fixture
def repo_api(base_url, auth_headers):
    """Fixture that returns a RepositoryAPI client"""
    client = BaseApiClient(base_url=base_url, headers=auth_headers)
    return RepositoryApiHelpers(client)