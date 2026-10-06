import os
import base64
from config import ENV, BROWSER
from datetime import datetime
import sys
import platform
import pytest
import allure
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
    # Login only once per worker/session
    if page.locator("input[name='login']").count() > 0:
        login = LoginPage(page)
        login.login()

    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot on test failure and attach it
    to both HTML and Allure reports.
    """

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = (
            item.funcargs.get("page")
            or item.funcargs.get("logged_in_page")
        )

        if page:

            screenshot_dir = os.path.join(
                "reports",
                "screenshots"
            )

            os.makedirs(
                screenshot_dir,
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            screenshot_path = os.path.join(
                screenshot_dir,
                f"{item.name}_{timestamp}.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            # Attach screenshot to HTML report
            with open(
                screenshot_path,
                "rb"
            ) as image_file:

                encoded_image = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            extra = getattr(
                report,
                "extras",
                []
            )

            extra.append(
                extras.png(encoded_image)
            )

            report.extras = extra

            # Attach screenshot to Allure
            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            print("\n" + "=" * 70)
            print(
                f"Screenshot Saved : "
                f"{screenshot_path}"
            )
            print("=" * 70 + "\n")

def pytest_sessionfinish(session, exitstatus):
    allure_result_dir = "reports/allure-result"
    os.makedirs(allure_result_dir, exist_ok=True)

    environment_file = os.path.join(
        allure_result_dir,
        "environment.properties"
    )

    environment_data = {
        "Environment": ENV,
        "Browser": BROWSER,
        "Python": sys.version.split()[0],
        "OS": platform.system(),
        "Platform": platform.platform(),
    }

    with open(environment_file, "w", encoding="utf-8") as file:
        for key, value in environment_data.items():
            file.write(f"{key}={value}\n")