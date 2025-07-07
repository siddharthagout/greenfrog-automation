"""constants config file with all params and constant informations"""

import os
from dotenv import load_dotenv

load_dotenv()


class EnvironmentParams:
    """class with all environmental params, it is reading confs form .env file in repo"""

    BASE_URL = os.getenv("BASE_URL")
    XRAY_URL = os.getenv("XRAY_URL")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    DOMAIN = os.getenv("DOMAIN")
    AUTH_HEADER = {
        "Authorization": f"Basic {os.getenv('AUTH_TOKEN')}",
        "Content-Type": "application/json",
    }


class JFrogEndpoints:
    """JFrog endpoints class"""

    REPO_ENDPOINT = "/artifactory/api/repositories"
    POLICY_ENDPOINT = "/xray/api/v2/policies"
    WATCH_ENDPOINT = "/xray/api/v2/watches"
    APPLY_WATCH_ENDPOINT = "/xray/api/v1/applyWatch"
    SCAN_STATUS_ENDPOINT = "/xray/api/v1/artifact/status"
    VIOLATIONS_ENDPOINT = "/xray/api/v1/violations"


class ApiTestConfs:
    """API test related configs"""

    REPO_PREFIX = "sid-jfrog-assignment-test-repo-"
    POLICY_PREFIX = "auto-policy-"
    WATCH_PREFIX = "auto-watch-"
    ARTIFACT_PATH = "/alpine/3.9/manifest.json"


class UITestConfs:
    pass
