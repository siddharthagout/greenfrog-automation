"""Factory to create the API request payload"""


class ApiPayloadFactory:
    """payload factory for backend APIs payload creation"""

    @staticmethod
    def create_repository_payload(repo_name):
        """factory method for creating repository payload"""
        return {
            "key": repo_name,
            "projectKey": "",
            "packageType": "docker",
            "rclass": "local",
            "xrayIndex": True,
        }

    @staticmethod
    def create_policy_payload(policy_name):
        """factory method for creating policy payload"""
        return {
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

    @staticmethod
    def create_watch_payload(policy_name, watch_name, repo_name):
        """factory method for creating watch payload"""
        return {
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

    @staticmethod
    def apply_watch_payload(watch_name, watch_start_date, watch_end_date):
        """factory method for applying watch payload"""
        return {
            "watch_names": [watch_name],
            "date_range": {
                "start_date": watch_start_date,
                "end_date": watch_end_date,
            },
        }

    @staticmethod
    def get_scan_status_payload(repo_name):
        """factory method for fetching scan status payload"""
        return {
            "repo": repo_name,
            "path": "/alpine/3.9/manifest.json",
        }

    @staticmethod
    def get_violations_payload(repo_name, watch_name, artifact_path):
        """factory method for fetching violations payload"""
        return {
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
