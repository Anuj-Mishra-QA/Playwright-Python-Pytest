from pages.login_page import LoginPage


def test_login(page):

    login = LoginPage(page)
    login.login()