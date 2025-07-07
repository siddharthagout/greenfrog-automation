import logging

from factories.data.payload_factory import ApiPayloadFactory
from config.constants import JFrogEndpoints


class JfrogApiHelpers:
    def __init__(self, api_client):
        self.client = api_client

    def create_repository(self, repo_name):
        """helper method for creating the repository with given repo_name"""
        payload = ApiPayloadFactory.create_repository_payload(repo_name)
        logging.info(
            "Sending PUT request to %s with payload: %s",
            JFrogEndpoints.REPO_ENDPOINT,
            payload,
        )

        try:
            logging.info("creating repository : %s", repo_name)
            response = self.client.put(
                JFrogEndpoints.REPO_ENDPOINT + "/" + repo_name, data=payload
            )
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
        """helper method to fetch all repository created in system"""
        logging.info("Sending GET request to %s", JFrogEndpoints.REPO_ENDPOINT)

        try:
            response = self.client.get(JFrogEndpoints.REPO_ENDPOINT)
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
        """helper method to create the policy with given policy name"""
        try:
            logging.info("creating policy : %s", policy_name)
            response = self.client.post(
                JFrogEndpoints.POLICY_ENDPOINT,
                data=ApiPayloadFactory.create_policy_payload(policy_name),
            )
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
        """helper method to create watch with given policy_name, watch_name, repo_name"""
        try:
            logging.info(
                "creating watch as - %s for %s repository", watch_name, repo_name
            )
            response = self.client.post(
                JFrogEndpoints.WATCH_ENDPOINT,
                data=ApiPayloadFactory.create_watch_payload(
                    policy_name, watch_name, repo_name
                ),
            )
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
        """helper method to apply given watch for a certain time period"""
        try:
            logging.info(
                "applying watch - %s for timerange %s to %s",
                watch_name,
                watch_start_date,
                watch_end_date,
            )
            response = self.client.post(
                JFrogEndpoints.APPLY_WATCH_ENDPOINT,
                data=ApiPayloadFactory.apply_watch_payload(
                    watch_name, watch_start_date, watch_end_date
                ),
            )
            logging.info("Response status for applywatch: %s", response.status_code)
            logging.info(
                "Response body for applywatch: %s", getattr(response, "text", response)
            )
            return response
        except Exception as e:
            logging.error("Error during applying watch: %s", str(e), exc_info=True)
            raise

    def get_scan_status(self, repo_name):
        """helper method to check the vulnerability scan status for given repo_name"""
        try:
            logging.info("checking scan status for repo : %s", repo_name)
            response = self.client.post(
                JFrogEndpoints.SCAN_STATUS_ENDPOINT,
                data=ApiPayloadFactory.get_scan_status_payload(repo_name),
            )
            logging.info("Response status for scan status: %s", response.status_code)
            logging.info(
                "Response body for scan status: %s", getattr(response, "text", response)
            )
            return response
        except Exception as e:
            logging.error("Error during scan status: %s", str(e), exc_info=True)
            raise

    def get_violations(self, repo_name, watch_name, artifact_path):
        """helper method to check the violations under a watch for
        a certain artifact for given repo_name
        """
        try:
            logging.info(
                "fetching violations for repo : %s with watch : %s and artifact : %s",
                repo_name,
                watch_name,
                artifact_path,
            )
            response = self.client.post(
                JFrogEndpoints.VIOLATIONS_ENDPOINT,
                data=ApiPayloadFactory.get_violations_payload(
                    repo_name, watch_name, artifact_path
                ),
            )
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
