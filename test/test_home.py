from pages.home_page import HomePage


def test_home_navigation(logged_in_page):

    home = HomePage(logged_in_page)

    home.go_home()

    home.open_sales()
    home.open_products()
    home.open_customers()
    home.open_quotations()
    home.go_home()
    home.open_purchase()