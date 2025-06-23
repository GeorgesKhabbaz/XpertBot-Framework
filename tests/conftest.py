"""
conftest.py
This module contains pytest fixtures used for setting up and tearing down the test environment.
Currently includes a fixture to launch and quit the Chrome browser for UI testing.
"""
import os
import re
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Define a fixture that will be executed once per class using the scope="class" argument
@pytest.fixture(scope="class")
def launchbrowser(request):
    """
    Fixture to launch Chrome browser in headless mode.
    Optimized for CI (GitHub Actions) – avoids user-data-dir issues.
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # optional but helpful

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://xpertbotacademy.online/nova/login")

    # Attach the driver to the test class so it can be accessed using self.driver inside tests
    request.cls.driver = driver

    # Yield pauses here to allow the test(s) to execute using the driver
    yield

    # Once all tests in the class are done, quit the browser to close the session
    driver.quit()


# pylint: disable=global-variable-undefined
def pytest_configure(config):
    """
    Pytest hook to configure HTML reporting and register the plugin.
    """
    global pytest_html
    pytest_html = config.pluginmanager.getplugin('html')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call): # pylint: disable=unused-argument
    """
    Hook to capture screenshots on test failure and attach them to the HTML report.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' and report.failed:
        try:
            driver = item.cls.driver

            safe_nodeid = re.sub(r'[\[\]\/\\:]', '_', report.nodeid)
            file_name = f"{safe_nodeid}.png"

            report_dir = os.path.dirname(item.config.option.htmlpath)
            screenshot_path = os.path.join(report_dir, file_name)

            driver.save_screenshot(screenshot_path)

            if os.path.exists(screenshot_path):
                html = (
                    f'<div><img src="{file_name}" alt="screenshot" '
                    f'style="width:400px;height:200px;" '
                    f'onclick="window.open(this.src)" align="right"/></div>'
                )
                extra.append(pytest_html.extras.html(html))

        except WebDriverException as e:
            print(f"[!] Could not attach screenshot: {e}")

    report.extras = extra
