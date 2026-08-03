from pages.home_page import HomePage
from pages.quotation_page import QuotationPage


def test_sales_order_flow(logged_in_page):

    home = HomePage(logged_in_page)
    quotation = QuotationPage(logged_in_page)

    home.go_home()

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