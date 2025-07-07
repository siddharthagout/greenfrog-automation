"""
Description : JFrog platform e2e test for xray feature testing using API and UI
"""

import json
import time
import logging
import subprocess
import allure
import pytest

from config.constants import EnvironmentParams, ApiTestConfs

from src.utils.scan_utils import wait_for_scan_done
from utils.screenshot_utils import capture_step

from factories.pages.login_page_factory import LoginPageFactory
from factories.pages.scan_page_factory import ScanPageFactory

from validators.response_validators import ResponseValidator


class TestRepositoryCRUD:
    """Test class for JFrog repository CRUD testcases"""

    @pytest.mark.sanity
    @pytest.mark.e2e
    @pytest.mark.api
    @allure.description(
        "Check if user is able to create repository and find \
            created repository in get response."
    )
    def test_create_repository(self, repo_api, repo_name):
        """Test repository creation"""
        # creating new repository
        response = repo_api.create_repository(repo_name)

        # Validating repository creation
        ResponseValidator.validate_status_code(response, 200)
        ResponseValidator.validate_status_message(
            response, f"Successfully created repository '{repo_name}'"
        )

        # Fetching response from get repository API
        get_repo_resp = repo_api.get_repositories()
        get_object = json.loads(get_repo_resp.text)

        repo_list = []
        for i in range(0, len(get_object)):
            repo_list.append(get_object[i]["key"])
        assert repo_name in repo_list, "Repo name not found in get API response"

    @pytest.mark.api
    @pytest.mark.e2e
    @allure.description("Push docker image into created repository")
    def test_push_image(self, repo_name):
        repo = repo_name
        domain = EnvironmentParams.DOMAIN
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
                EnvironmentParams.USERNAME,
                "-p",
                EnvironmentParams.PASSWORD,
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
    @pytest.mark.e2e
    @allure.description("Check if user is able to create policy.")
    def test_create_policy(self, repo_api, policy_name):
        # creating policy
        response = repo_api.create_policy(policy_name)

        # Validating policy creationg
        ResponseValidator.validate_status_code(response, 201)
        ResponseValidator.validate_status_message(
            response, "Policy created successfully"
        )

    @pytest.mark.api
    @pytest.mark.e2e
    @allure.description("Verify if user can create watch with a policy and repo")
    def test_create_watch(self, repo_api, policy_name, watch_name, repo_name):
        # creating watch
        response = repo_api.create_watch(policy_name, watch_name, repo_name)

        # validating creating watch
        ResponseValidator.validate_status_code(response, 201)
        ResponseValidator.validate_status_message(
            response, "Watch has been successfully created"
        )

    @pytest.mark.api
    @pytest.mark.e2e
    @allure.description("Apply watch to existing content")
    def test_apply_watch(self, watch_name, repo_api, watch_start_date, watch_end_date):
        # applying watch watch
        response = repo_api.apply_watch(watch_name, watch_start_date, watch_end_date)

        # Validating apply watch action
        ResponseValidator.validate_status_code(response, 202)
        ResponseValidator.validate_status_message(
            response, "History Scan is in progress"
        )

    @pytest.mark.api
    @pytest.mark.e2e
    @allure.description("Apply watch to existing content")
    def test_scan_status(self, repo_api, repo_name):
        # Wait until scan is DONE or timeout occurs
        response = wait_for_scan_done(repo_api, repo_name)

        # Optional: validate again if needed
        assert response.json().get("overall", {}).get("status") == "DONE"

    @pytest.mark.api
    @pytest.mark.e2e
    @allure.description("Check violations status")
    def test_violations_status(self, repo_api, repo_name, watch_name):
        # fetching scan status
        artifact_path = ApiTestConfs.ARTIFACT_PATH
        response = repo_api.get_violations(repo_name, watch_name, artifact_path)

        # Validating violation status
        ResponseValidator.validate_status_code(response, 200)
        ResponseValidator.validate_field_value_in_response(
            response, "total_violations", 0
        )


class TestXrayViolationUI:

    @pytest.mark.ui
    @pytest.mark.e2e
    @allure.description("Verify violations for a given reponame")
    def test_verify_scan_violations_ui(self, driver, repo_name):
        platform_url = EnvironmentParams.BASE_URL
        username = EnvironmentParams.USERNAME
        password = EnvironmentParams.PASSWORD

        login_page = LoginPageFactory(driver)
        scan_page = ScanPageFactory(driver)

        # Opening browser and login
        driver.get(f"{platform_url}ui/login")
        capture_step(driver, "01_login_page_loaded")

        login_page.login(username, password)
        capture_step(driver, "02_after_login")

        # Going to the violations page directly
        time.sleep(5)  # waiting for login to complete
        scan_url = (
            f"{platform_url}ui/scans-list/repositories/{repo_name}/scan-descendants"
        )
        driver.get(scan_url)

        # Clicking on uploaded image and open policy violations
        scan_page.wait_and_click_image()
        capture_step(driver, "03_image_clicked")

        scan_page.open_policy_violations()
        capture_step(driver, "04_policy_tab_opened")

        # Validating only high or critical severities
        scan_page.verify_violation_severity()
        capture_step(driver, "05_violation_verified")
