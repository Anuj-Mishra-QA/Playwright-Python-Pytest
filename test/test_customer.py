from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.customer_page import CustomerPage


def test_create_customer(page):

    login = LoginPage(page)
    home = HomePage(page)
    customer = CustomerPage(page)

    login.login()

    home.open_sales()
    home.open_customers()

    customer.new_customer()
    customer.select_person()

    customer_name = customer.enter_customer_name()
    customer_email = customer.enter_email()

    customer.select_country("United States")
    customer.save_customer()

    assert customer_name.startswith("Automation_Customer_")
    assert customer_email.endswith("@gmail.com")