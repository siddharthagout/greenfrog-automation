"""
Description : JFrog respository CRUD operations tests
"""

import json
import allure
import pytest
import subprocess
import logging
import time
from config import settings


class TestRepositoryCRUD:
    """Test class for JFrog repository CRUD testcases"""

    @pytest.mark.sanity
    @pytest.mark.api
    @allure.description(
        "Check if user is able to create repository and find created repository in get response."
    )
    def test_create_repository(self, repo_api, repo_name):
        """Test repository creation"""
        # creating new repository
        response = repo_api.create_repository(repo_name)
        assert response.status_code in [200, 201], "Failed to create repository"

        # Fetching response from get repository API
        get_repo_resp = repo_api.get_repositories()
        get_object = json.loads(get_repo_resp.text)

        repo_list = []
        for i in range(0, len(get_object)):
            repo_list.append(get_object[i]["key"])

        assert repo_name in repo_list, "Repo name not found in get API response"

    @pytest.mark.api
    @allure.description("Push docker image into created repository")
    def test_push_image(self, repo_name):
        repo = repo_name
        domain = settings.DOMAIN
        image = "alpine:3.9"
        tag = f"{domain}/{repo}/{image}"

        # Pulling image
        logging.info("pulling image : %s", image)
        subprocess.run(["docker", "pull", image], check=True)

        # Login to artifactory
        logging.info("Logging into the repository")
        subprocess.run(
            [
                "docker",
                "login",
                domain,
                "-u",
                settings.USERNAME,
                "-p",
                settings.PASSWORD,
            ],
            check=True,
        )

        # tagging image
        logging.info("creating image tag")
        subprocess.run(["docker", "tag", image, tag], check=True)

        # pushing image to artifactory
        logging.info("pushing image to the repository")
        subprocess.run(["docker", "push", tag], check=True)
        logging.info("image pushed to the repository")

    @pytest.mark.api
    @allure.description("Check if user is able to create policy.")
    def test_create_policy(self, repo_api, policy_name):
        # creating policy
        response = repo_api.create_policy(policy_name)
        assert response.status_code in [200, 201], "Policy not created"

    @pytest.mark.api
    @allure.description("Verify if user can create watch with a policy and repo")
    def test_create_watch(self, repo_api, policy_name, watch_name, repo_name):
        # creating watch
        response = repo_api.create_watch(policy_name, watch_name, repo_name)

        assert response.status_code in [200, 201], "watch not created"

    @pytest.mark.api
    @allure.description("Apply watch to existing content")
    def test_apply_watch(self, watch_name, repo_api, watch_start_date, watch_end_date):
        # applying watch watch
        response = repo_api.apply_watch(watch_name, watch_start_date, watch_end_date)

        assert response.status_code in [
            201,
            202,
        ], "watch not applied to the content"

    @pytest.mark.api
    @allure.description("Apply watch to existing content")
    def test_scan_status(self, repo_api, repo_name):
        # fetching scan status

        MAX_WAIT = 60
        INTERVAL = 5
        start_time = time.time()
        status = None

        # retying the scan status to get the status as DONE
        while time.time() - start_time < MAX_WAIT:
            response = repo_api.get_scan_status(repo_name)
            assert response.status_code == 200, "Scan status API failed"

            json_object = response.json()
            status = json_object.get("overall", {}).get("status", None)

            if status == "DONE":
                break

            time.sleep(INTERVAL)

        # validating if status is DONe
        assert status == "DONE", f"Scan did not complete in {MAX_WAIT} seconds"

    @pytest.mark.api
    @allure.description("Check violations status")
    def test_violations_status(self, repo_api, repo_name, watch_name):
        # fetching scan status
        artifact_path = "/alpine/3.9/manifest.json"
        response = repo_api.get_violations(repo_name, watch_name, artifact_path)
        assert response.status_code == 200, "Scan status API failed"

        json_object = response.json()
        violations = json_object.get("total_violations")
        assert violations > 0, "No violations found"
