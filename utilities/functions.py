"""
functions.py
This module contains utility functions for the XpertBot framework,
including actions like logging in to the XpertBot Academy platform.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Importing the automation logger class for logging
from utilities.utils import AutomationLoggerClass
# Importing the credentials module for locators
from pages import creds


def xpertbot_login_function(self, username, password):
    """
    Simulates the login action for XpertBot Academy.
    Returns True upon successful execution.
    """
    log = AutomationLoggerClass.automation()

    email_locator = (By.XPATH, creds.EMAIL)
    password_locator = (By.XPATH, creds.PASSWORD)
    login_button_locator = (By.XPATH, creds.LOGIN_BUTTON)
    img_locator = (By.XPATH, creds.IMG)

    log.info("Locating email input field")
    try:
        log.info("Waiting for email input field to be visible...")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(email_locator))
        email_field = self.driver.find_element(*email_locator)
        email_field.clear()
        email_field.send_keys(username)
        log.info("Entered username.")

        password_field = self.driver.find_element(*password_locator)
        password_field.clear()
        password_field.send_keys(password)
        log.info("Entered password.")

        login_button = self.driver.find_element(*login_button_locator)
        login_button.click()
        log.info("Clicked login button.")

        time.sleep(2)

        # Check for an element that appears only when login is successful

        log.info("Waiting for image logo to confirm login...")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(img_locator)
        )
        log.info("Profile image found. Login was successful.")

        return True

    except (NoSuchElementException, TimeoutException) as e:
        log.error("Error during login sequence: %s", e)
        return False


def xpertbot_logout_function(self):
    """
    Performs logout from the XpertBot Academy platform.
    """
    log = AutomationLoggerClass.automation()
    profile_button_locator = (By.XPATH, creds.PROFILE_BUTTON)
    logout_button_locator = (By.XPATH, creds.LOGOUT_BUTTON)

    try:
        log.info("Attempting to locate profile dropdown button...")
        profile_button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((profile_button_locator)))
        profile_button.click()
        log.info("Clicked on profile dropdown.")

        log.info("Waiting for logout link...")
        logout_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((logout_button_locator)))
        logout_link.click()
        log.info("Clicked logout link. User should be logged out.")

        time.sleep(2)
        return True

    except (NoSuchElementException, TimeoutException) as e:
        log.error("Logout failed: %s", e)
        return False
