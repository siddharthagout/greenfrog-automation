"""Recurring scan status validator util file"""

from src.validators.response_validators import ResponseValidator


def check_scan_done(response):
    """validation if scan is done or not"""
    ResponseValidator.validate_status_code(response, 200)
    status = response.json().get("overall", {}).get("status")
    return status == "DONE", status


def wait_for_scan_done(repo_api, repo_name, timeout=120, interval=5):
    """
    Retry until scan status becomes DONE or timeout.
    Returns final response.
    Raises AssertionError if not DONE in time.
    """
    return ResponseValidator.validate_with_retry(
        func=lambda: repo_api.get_scan_status(repo_name),
        check_func=check_scan_done,
        timeout=timeout,
        interval=interval,
        description=f"Waiting for scan to be DONE for repo: {repo_name}",
    )
