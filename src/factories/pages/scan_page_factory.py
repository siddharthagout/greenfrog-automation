"""Scan page factory elemements on scan page"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScanPageElements:
    """Scan Page Element paths"""

    UPLOADED_IMAGE_XPATH = '//div[@data-cy="alpine/3.9"]'
    POLICY_PAGE_XPATH = '//span[@id="menuItemText" and contains(normalize-space(), "Policy Violations")]'
    VIOLATION_SEVERETY_XPATH = '//div[contains(@class, "severity-template-container") \and .//div[contains(@class, "xray-svg")]]'


class ScanPageFactory:
    """Scan page factory"""

    def __init__(self, driver):
        self.driver = driver

    def wait_and_click_image(self):
        """method for clicking on uploaded docker image"""
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, ScanPageElements.UPLOADED_IMAGE_XPATH)
            )
        ).click()

    def open_policy_violations(self):
        """method for clicking policy violation page"""
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    ScanPageElements.POLICY_PAGE_XPATH,
                )
            )
        ).click()

    def verify_violation_severity(self):
        """method for checking violation severity"""
        containers = self.driver.find_elements(
            By.XPATH, ScanPageElements.VIOLATION_SEVERETY_XPATH
        )

        for container in containers:
            try:
                label = container.find_element(By.XPATH, ".//span")
                severity_text = label.text.strip().lower()
                assert severity_text in [
                    "high",
                    "critical",
                ], f"Unexpected severity: {severity_text}"
            except Exception as e:
                raise AssertionError(f"Could not verify severity: {e}")
