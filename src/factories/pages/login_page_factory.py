"""Login page factory for Login related elements"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPageElements:
    """Login Page Element paths"""

    LOGIN_BUTTON_XPATH = '//*[@id="app"]/div[2]/div/div/div/div[2]/div/div[2]/div/div/form/div[2]/div[4]/div'


class LoginPageFactory:
    """Login page factory"""

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        """login function"""
        wait = WebDriverWait(self.driver, 20)

        # Wait for username field
        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_input.send_keys(username)

        # Wait for password input
        password_input = wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(password)

        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, LoginPageElements.LOGIN_BUTTON_XPATH))
        )

        login_button.click()
