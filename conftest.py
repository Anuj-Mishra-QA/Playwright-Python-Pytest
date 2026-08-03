import os
import base64
from datetime import datetime

import pytest
from pytest_html import extras

from utils.browser_manager import BrowserManager
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def page():

    _, _, _, page = BrowserManager.get_page()

    yield page

    BrowserManager.close_browser()


@pytest.fixture(scope="session")
def logged_in_page(page):

    # Login only once per session
    if page.locator("input[name='login']").count() > 0:
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

            screenshot_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            screenshot_path = os.path.join(
                screenshot_dir,
                f"{item.name}_{timestamp}.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            with open(screenshot_path, "rb") as image_file:
                encoded_image = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            extra = getattr(report, "extras", [])
            extra.append(extras.png(encoded_image))
            report.extras = extra

            print("\n" + "=" * 70)
            print(f"Screenshot Saved : {screenshot_path}")
            print("=" * 70 + "\n")