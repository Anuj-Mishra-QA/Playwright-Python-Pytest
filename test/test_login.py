from pages.login_page import LoginPage
from pages.home_page import HomePage


def test_home_navigation(page):

    login = LoginPage(page)
    home = HomePage(page)

    login.login()

    home.open_sales()
    home.open_products()
    home.open_customers()
    home.open_quotations()