from utils.browser import Browser

from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.inventory_page import InventoryPage
from pages.customer_page import CustomerPage
from pages.quotation_page import QuotationPage


def main():

    playwright, browser, page = Browser.launch_browser()

    # Page Objects
    login = LoginPage(page)
    home = HomePage(page)
    product = ProductPage(page)
    inventory = InventoryPage(page)
    customer = CustomerPage(page)
    quotation = QuotationPage(page)

    # Login
    login.login()

    # Open Sales Module
    home.open_sales()

    # ---------------- Product ----------------

    home.open_products()
    product_name = product.create_product()
    inventory.enter_inventory_quantity(100)
    inventory.verify_quantity_on_hand()

    # ---------------- Customer ----------------

    home.open_customers()
    customer.new_customer()
    customer.select_person()
    customer_name = customer.enter_customer_name()
    customer_email = customer.enter_email()
    customer.enter_email()
    customer.verify_email()
    customer.select_country("United States")
    customer.save_customer()

    # ---------------- Quotation ----------------

    quotation.new_quotation()
    quotation.select_customer(customer_name)
    quotation.add_product(product_name)
    quotation.enter_quantity()
    quotation.verify_amount()
    # quotation.send_quotation(customer_name)
    # quotation.send_quotation(customer_email)
    quotation.confirm_order()
    quotation.open_delivery()
    quotation.create_Regular_invoice()
    page.wait_for_timeout(5000)
    browser.close()
    playwright.stop()




if __name__ == "__main__":
    main()