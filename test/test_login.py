from config import URL
from pages.login_page import LoginPage


def test_login(page):
    page.goto(URL)
    page.wait_for_load_state("domcontentloaded")

    login = LoginPage(page)
    login.login()