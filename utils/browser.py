from playwright.sync_api import sync_playwright
from config import URL, HEADLESS, SLOW_MO


class Browser:

    @staticmethod
    def launch_browser():
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )

        page = browser.new_page()
        page.goto(URL)

        page.wait_for_load_state("domcontentloaded")

        print("Browser launched successfully")

        return playwright, browser, page