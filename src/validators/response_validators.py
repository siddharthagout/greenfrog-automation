"""Validator class for http attributes from tests"""

import time
import json
import logging
import allure


class ResponseValidator:

    @staticmethod
    def validate_status_code(response, expected_code):
        """Validate status code function"""
        logging.info("Response Status Code: %s", response.status_code)
        with allure.step(f"Validating status code {expected_code}"):
            assert (
                response.status_code == expected_code
            ), f"Expected {expected_code}, got {response.status_code}"

    @staticmethod
    def validate_status_message(response, expected_message):
        """Validate status code function"""
        with allure.step(f"Validating status message : {expected_message}"):
            assert (
                expected_message in response.text
            ), f"Expected :  {expected_message}, but got : {response.text}"

    @staticmethod
    def validate_response_json(response):
        """Validate Json response type check"""
        with allure.step("Validating response body is in JSON format"):
            assert (
                "application/json" in response.headers["content-type"]
            ), "Response is not JSON"
            assert response.json() is not None, "Empty JSON response"

    @staticmethod
    def validate_field_value_in_response(response, field_name, expected_value):
        """Helper function to check actual and expected value at root level with partial string matching."""
        with allure.step("Checking asserts for API response"):
            response_dict = json.loads(response.text)
            actual_value = response_dict.get(field_name)

            assert (
                actual_value is not None
            ), f"Field '{field_name}' not found in response."

            if isinstance(actual_value, list):
                assert any(
                    str(expected_value) in str(item) for item in actual_value
                ), f"Expected value '{expected_value}' not found in list {actual_value} for field '{field_name}'"
            elif isinstance(actual_value, str) and isinstance(expected_value, str):
                assert (
                    expected_value in actual_value
                ), f"Expected substring '{expected_value}' not found in '{actual_value}' for field '{field_name}'"
            else:
                assert str(expected_value) == str(
                    actual_value
                ), f"Expected '{expected_value}' but found '{actual_value}' for field '{field_name}'"

    @staticmethod
    def validate_with_retry(func, check_func, timeout=120, interval=5, description=""):
        """
        Retry a function until check_func returns True or timeout is reached.
        - func: function to call repeatedly (e.g. API call)
        - check_func: returns (True, result) or (False, result)
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = func()
            try:
                passed, result = check_func(response)
                if passed:
                    return response
            except Exception as e:
                logging.warning(f"{description} - check failed: {e}")
            time.sleep(interval)
        raise AssertionError(f"{description} failed after {timeout} seconds")

    @staticmethod
    def validate_scan_done(scan_response_json):
        assert (
            scan_response_json.get("overall", {}).get("status") == "DONE"
        ), "Scan is not complete (overall.status != DONE)"
