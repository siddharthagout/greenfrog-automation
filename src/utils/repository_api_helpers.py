import logging


class RepositoryApiHelpers:
    def __init__(self, api_client):
        self.client = api_client

    def create_repository(self, repo_key):
        endpoint = f"/artifactory/api/repositories/{repo_key}"
        payload = {
            "key": repo_key,
            "projectKey": "",
            "packageType": "docker",
            "rclass": "local",
            "xrayIndex": True,
        }

        logging.info("Sending PUT request to %s with payload: %s", endpoint, payload)

        try:
            response = self.client.put(endpoint, data=payload)
            logging.info("Response status: %s", response.status_code)
            logging.info("Response body: %s", getattr(response, "text", response))
            return response
        except Exception as e:
            logging.error("Error during create_repository: %s", str(e), exc_info=True)
            raise

    def get_repositories(self):
        endpoint = "/artifactory/api/repositories"
        logging.info("Sending GET request to %s", endpoint)

        try:
            response = self.client.get(endpoint)
            logging.info("Response status: %s", response.status_code)
            logging.info("Response body: %s", getattr(response, "text", response))
            return response
        except Exception as e:
            logging.error("Error during get_repositories: %s", str(e), exc_info=True)
            raise
