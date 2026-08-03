from utils.browser import Browser


class BrowserManager:
    playwright = None
    browser = None
    context = None
    page = None

    @classmethod
    def get_page(cls):

        if cls.page is None:
            cls.playwright, cls.browser, cls.context, cls.page = Browser.launch_browser()

        return (
            cls.playwright,
            cls.browser,
            cls.context,
            cls.page
        )

    @classmethod
    def close_browser(cls):

        if cls.context:
            cls.context.close()

        if cls.browser:
            cls.browser.close()

        if cls.playwright:
            cls.playwright.stop()

        cls.playwright = None
        cls.browser = None
        cls.context = None
        cls.page = None