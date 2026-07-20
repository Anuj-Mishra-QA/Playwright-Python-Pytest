import os
from datetime import datetime

import pytest
from utils.browser import Browser


@pytest.fixture
def page():
    # Launch Browser
    playwright, browser, page = Browser.launch_browser()

    yield page

    # Close Browser
    browser.close()
    playwright.stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically capture screenshot whenever a test fails.
    """
    outcome = yield
    report = outcome.get_result()

    # Take screenshot only when test execution fails
    if report.when == "call" and report.failed:

        page = item.funcargs.get("page", None)

        if page:

            # Create reports/screenshots folder if it doesn't exist
            screenshot_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            # Screenshot name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            screenshot_path = os.path.join(
                screenshot_dir,
                f"{item.name}_{timestamp}.png"
            )

            # Capture screenshot
            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            print("\n" + "=" * 70)
            print(f"Screenshot Saved : {screenshot_path}")
            print("=" * 70 + "\n")