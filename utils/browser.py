from playwright.sync_api import sync_playwright
from config import (
    URL,
    HEADLESS,
    SLOW_MO,
    VIDEO,
    VIDEO_PATH,
    BROWSER
)


class Browser:

    @staticmethod
    def launch_browser():

        playwright = sync_playwright().start()

        browser_name = BROWSER.lower().strip()

        if browser_name == "chrome":

            browser = playwright.chromium.launch(
                channel="chrome",
                headless=HEADLESS,
                slow_mo=SLOW_MO
            )

            print("CHROME browser launched successfully")

        elif browser_name == "firefox":

            browser = playwright.firefox.launch(
                headless=HEADLESS,
                slow_mo=SLOW_MO
            )

            print("FIREFOX browser launched successfully")

        else:

            playwright.stop()

            raise ValueError(
                f"Unsupported browser: {BROWSER}. "
                f"Use 'chrome' or 'firefox'."
            )

        # Video Recording
        if VIDEO:

            context = browser.new_context(
                record_video_dir=VIDEO_PATH
            )

        else:

            context = browser.new_context()

        page = context.new_page()

        page.goto(URL)

        page.wait_for_load_state("domcontentloaded")

        return playwright, browser, context, page