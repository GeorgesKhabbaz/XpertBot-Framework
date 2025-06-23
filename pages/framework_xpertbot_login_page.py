"""
framework_xpertbot_login_page.py
Page Object Model class for XpertBot Academy login page.
Handles the login process by delegating to a reusable function.
"""

# Importing the login function
from utilities.functions import xpertbot_login_function, xpertbot_logout_function

class FrameworkXpertBotLoginPageClass:
    """
    Page class that encapsulates actions and elements of the XpertBot Academy login page.
    """

    def __init__(self, driver):
        """
        Initializes the login page with the provided WebDriver instance.

        :param driver: Selenium WebDriver object
        """
        self.driver = driver

    def xpertbot_login(self, username, password):  # Page of XpertBot Login
        """
        Calls the login function to perform the login steps.
        """
        return xpertbot_login_function(self, username, password)

    def xpertbot_signup(self):  # another page
        """
        Calls the signup function to perform the signup steps.
        """
        raise NotImplementedError("Signup functionality is not yet implemented.")

    def xpertbot_logout(self):
        """
        Calls the logout function to perform the logout steps.
        """
        xpertbot_logout_function(self)
