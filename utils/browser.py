from playwright.sync_api import sync_playwright
from config import URL, HEADLESS, SLOW_MO, VIDEO, VIDEO_PATH


class Browser:

    @staticmethod
    def launch_browser():
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )

        # Enable / Disable Video Recording
        if VIDEO:
            context = browser.new_context(
                record_video_dir=VIDEO_PATH
            )
        else:
            context = browser.new_context()

        page = context.new_page()
        page.goto(URL)

        page.wait_for_load_state("domcontentloaded")

        print("Browser launched successfully")

        return playwright, browser, context, page