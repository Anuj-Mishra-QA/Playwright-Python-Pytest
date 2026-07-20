from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.quotation_page import QuotationPage


def test_sales_order_flow(page):

    login = LoginPage(page)
    home = HomePage(page)
    quotation = QuotationPage(page)

    login.login()

    home.open_sales()

    quotation.new_quotation()

    quotation.select_customer()

    quotation.add_product()

    quotation.enter_quantity()

    amount = quotation.verify_amount()

    quotation.confirm_order()

    quotation.open_delivery()

    quotation.create_regular_invoice()

    assert amount["total"] != ""