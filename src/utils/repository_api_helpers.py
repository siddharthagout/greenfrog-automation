import logging


class RepositoryApiHelpers:
    def __init__(self, api_client):
        self.client = api_client

    def create_repository(self, repo_name):
        endpoint = f"/artifactory/api/repositories/{repo_name}"
        payload = {
            "key": repo_name,
            "projectKey": "",
            "packageType": "docker",
            "rclass": "local",
            "xrayIndex": True,
        }

        logging.info("Sending PUT request to %s with payload: %s", endpoint, payload)

        try:
            logging.info("creating repository : %s", repo_name)
            response = self.client.put(endpoint, data=payload)
            logging.info(
                "Response status for create repository: %s", response.status_code
            )
            logging.info(
                "Response body for create repository: %s",
                getattr(response, "text", response),
            )
            return response
        except Exception as e:
            logging.error("Error during create_repository: %s", str(e), exc_info=True)
            raise

    def get_repositories(self):
        endpoint = "/artifactory/api/repositories"
        logging.info("Sending GET request to %s", endpoint)

        try:
            response = self.client.get(endpoint)
            logging.info(
                "Response status for get repositories: %s", response.status_code
            )
            logging.info(
                "Response body for get repositories: %s",
                getattr(response, "text", response),
            )
            return response
        except Exception as e:
            logging.error("Error during get_repositories: %s", str(e), exc_info=True)
            raise

    def create_policy(self, policy_name):
        endpoint = "/xray/api/v2/policies"
        payload = {
            "name": policy_name,
            "description": "Auto-created security policy",
            "type": "Security",
            "rules": [
                {
                    "name": "rule-1",
                    "criteria": {
                        "min_severity": "High",
                        "malicious_package": False,
                        "fix_version_dependant": False,
                    },
                    "actions": {
                        "block_download": {"active": False},
                        "fail_build": False,
                    },
                    "priority": 1,
                }
            ],
        }

        try:
            logging.info("creating policy : %s", policy_name)
            response = self.client.post(endpoint, data=payload)
            logging.info("Response status for create policy: %s", response.status_code)
            logging.info(
                "Response body for create policy: %s",
                getattr(response, "text", response),
            )
            return response
        except Exception as e:
            logging.error("Error during creating policy: %s", str(e), exc_info=True)
            raise

    def create_watch(self, policy_name, watch_name, repo_name):
        endpoint = "/xray/api/v2/watches"
        payload = {
            "general_data": {
                "name": watch_name,
                "description": "This is an example watch #1",
                "active": True,
            },
            "project_resources": {
                "resources": [
                    {
                        "type": "repository",
                        "bin_mgr_id": "default",
                        "name": repo_name,
                        "filters": [{"type": "regex", "value": ".*"}],
                    }
                ]
            },
            "assigned_policies": [{"name": policy_name, "type": "security"}],
        }

        try:
            logging.info(
                "creating watch as - %s for %s repository", watch_name, repo_name
            )
            response = self.client.post(endpoint, data=payload)
            logging.info("Response status for create watch: %s", response.status_code)
            logging.info(
                "Response body for create watch: %s",
                getattr(response, "text", response),
            )
            return response
        except Exception as e:
            logging.error("Error during create watch: %s", str(e), exc_info=True)
            raise

    def apply_watch(self, watch_name, watch_start_date, watch_end_date):
        endpoint = "/xray/api/v1/applyWatch"
        payload = {
            "watch_names": [watch_name],
            "date_range": {
                "start_date": watch_start_date,
                "end_date": watch_end_date,
            },
        }

        try:
            logging.info(
                "applying watch - %s for timerange %s to %s",
                watch_name,
                watch_start_date,
                watch_end_date,
            )
            response = self.client.post(endpoint, data=payload)
            logging.info("Response status for applywatch: %s", response.status_code)
            logging.info(
                "Response body for applywatch: %s", getattr(response, "text", response)
            )
            return response
        except Exception as e:
            logging.error("Error during applying watch: %s", str(e), exc_info=True)
            raise

    def get_scan_status(self, repo_name):
        endpoint = "/xray/api/v1/artifact/status"
        payload = {
            "repo": repo_name,
            "path": "/alpine/3.9/manifest.json",
        }
        try:
            logging.info("checking scan status for repo : %s", repo_name)
            response = self.client.post(endpoint, data=payload)
            logging.info("Response status for scan status: %s", response.status_code)
            logging.info(
                "Response body for scan status: %s", getattr(response, "text", response)
            )
            return response
        except Exception as e:
            logging.error("Error during scan status: %s", str(e), exc_info=True)
            raise

    def get_violations(self, repo_name, watch_name, artifact_path):
        endpoint = "/xray/api/v1/violations"
        payload = {
            "filters": {
                "watch_name": watch_name,
                "violation_type": "Security",
                "min_severity": "High",
                "resources": {
                    "artifacts": [{"repo": repo_name, "path": artifact_path}]
                },
            },
            "pagination": {
                "order_by": "created",
                "direction": "asc",
                "limit": 100,
                "offset": 1,
            },
        }
        try:
            logging.info(
                "fetching violations for repo : %s with watch : %s and artifact : %s",
                repo_name,
                watch_name,
                artifact_path,
            )
            response = self.client.post(endpoint, data=payload)
            logging.info(
                "Response status for fetching violations: %s", response.status_code
            )
            logging.info(
                "Response body for fetching violations: %s",
                getattr(response, "text", response),
            )
            return response
        except Exception as e:
            logging.error(
                "Error during violations fetching status: %s", str(e), exc_info=True
            )
            raise
