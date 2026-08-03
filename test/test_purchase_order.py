from pages.home_page import HomePage
from pages.purchase_order_page import PurchasePage


def test_purchase(logged_in_page):

    home = HomePage(logged_in_page)
    purchase_order = PurchasePage(logged_in_page)

    home.go_home()

    home.open_purchase()

    purchase_order.new_rfq()
    purchase_order.select_vendor()
    purchase_order.add_product()
    purchase_order.enter_quantity()
    purchase_order.unit_price()
    purchase_order.verify_tax_details()
    purchase_order.confirm_order()
    purchase_order.receive_products()
