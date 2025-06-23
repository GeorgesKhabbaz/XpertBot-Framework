"""
test_frameworkxpertbotlogin.py
Test cases for logging into XpertBot Academy using Pytest and Page Object Model (POM).
"""

import pytest
from utilities.utils import AutomationLoggerClass, get_newest_excel_file
from pages.framework_xpertbot_login_page import FrameworkXpertBotLoginPageClass


@pytest.mark.usefixtures("launchbrowser")
class TestXpertBotLoginClass:
    """
    Test class for verifying the login and logout functionality of XpertBot Academy.
    """
    # pylint: disable=attribute-defined-outside-init

    def setup_method(self, _method):
        """
        Runs before each test method. Initializes the logger.
        """
        self.log = AutomationLoggerClass.automation()

    test_data_var = get_newest_excel_file()

    @pytest.mark.parametrize("testdata", test_data_var)
    def test_login(self, testdata):
        """
        Test login functionality followed by logout for XpertBot Academy.
        """
        try:
            # Maximize the browser window
            self.driver.maximize_window()  # pylint: disable=no-member

            self.log.info("Starting login test for: %s", testdata["username"])

            login_page = FrameworkXpertBotLoginPageClass(self.driver)  # pylint: disable=no-member

            # Perform login using the provided test data
            login_success = login_page.xpertbot_login(**testdata)

            assert login_success, f"Login failed for user: {testdata['username']}"
            self.log.info("Login successful for user: %s", testdata["username"])
            self.log.info("Starting logout test.")
            login_page.xpertbot_logout()
            self.log.info("Logout test executed successfully.")

        except AssertionError as ae:
            self.log.error(str(ae))
            raise
        except Exception as e:
            self.log.error("An error occurred during the login test: %s", e)
            raise
