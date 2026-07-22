import os
import base64
from datetime import datetime

import pytest
from pytest_html import extras

from utils.browser import Browser
from pages.login_page import LoginPage


@pytest.fixture
def page():
    # Launch Browser
    playwright, browser, context, page = Browser.launch_browser()

    yield page

    # Close Browser
    context.close()
    browser.close()
    playwright.stop()


@pytest.fixture
def logged_in_page(page):
    """
    Login before executing the test.
    """
    login = LoginPage(page)
    login.login()

    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot on test failure and attach it to HTML report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")

        if page:

            # Create screenshots directory
            screenshot_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            screenshot_path = os.path.join(
                screenshot_dir,
                f"{item.name}_{timestamp}.png"
            )

            # Save Screenshot
            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            # Convert image to Base64
            with open(screenshot_path, "rb") as image_file:
                encoded_image = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            # Attach Screenshot to HTML Report
            extra = getattr(report, "extras", [])

            extra.append(
                extras.png(encoded_image)
            )

            report.extras = extra

            print("\n" + "=" * 70)
            print(f"Screenshot Saved : {screenshot_path}")
            print("=" * 70 + "\n")