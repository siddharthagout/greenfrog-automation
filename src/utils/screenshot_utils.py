"""screenshot utility for taking screenshots"""

import os
import time
import allure


def capture_step(driver, step_name: str):
    """screenshot taking method"""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{step_name}_{timestamp}.png"
    filepath = os.path.join("screenshots", filename)

    # Ensure screenshots directory exists
    os.makedirs("screenshots", exist_ok=True)

    # Save and attach
    driver.save_screenshot(filepath)
    allure.attach.file(
        filepath, name=step_name, attachment_type=allure.attachment_type.PNG
    )
