"""
Description : JFrog respository CRUD operations tests
"""

import json
import allure
import pytest
import subprocess
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
        tag = f"{domain}/{repo}/alpine:3.9"

        # Pulling image
        subprocess.run(["docker", "pull", image], check=True)

        # Login to artifactory
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
        subprocess.run(["docker", "tag", image, tag], check=True)

        # pushing image to artifactory
        subprocess.run(["docker", "push", tag], check=True)
