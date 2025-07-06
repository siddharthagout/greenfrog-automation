"""
Description : JFrog respository CRUD operations tests
"""

import pytest


class TestRepositoryCRUD:
    """Test class for JFrog repository CRUD testcases"""

    @pytest.mark.sanity
    def test_create_repository(self, repo_api, repo_name):
        """Test repository creation"""
        response = repo_api.create_repository(repo_name)
        assert response.status_code in [200, 201], "Failed to create repository"
