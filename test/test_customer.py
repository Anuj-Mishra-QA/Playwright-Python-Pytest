import pytest
import allure

from pages.home_page import HomePage
from pages.customer_page import CustomerPage
from data.customer_data import CUSTOMER


def test_create_customer(logged_in_page):

    home = HomePage(logged_in_page)
    customer = CustomerPage(logged_in_page)

    home.go_home()

    home.open_sales()
    home.open_customers()

    customer_exists = customer.customer_exists_by_email(
        CUSTOMER["email"]
    )

    if customer_exists:

        with allure.step("Verify Customer Already Exists"):

            assert customer_exists is True, (
                f"Customer with email {CUSTOMER['email']} "
                f"was not found"
            )

            allure.attach(
                f"Customer Name : {CUSTOMER['name']}\n"
                f"Customer Email : {CUSTOMER['email']}\n"
                f"Status : Customer already exists",
                name="Existing Customer Validation",
                attachment_type=allure.attachment_type.TEXT
            )

        print(
            f"Customer already exists with email: "
            f"{CUSTOMER['email']}"
        )

        customer.open_existing_customer(
            CUSTOMER["email"]
        )

        customer.enter_customer_name()
        customer.enter_email()
        customer.select_country()
        customer.save_customer()

        print("Existing Customer Updated Successfully")

    else:

        customer.new_customer()
        customer.select_person()

        customer_name = customer.enter_customer_name()
        customer_email = customer.enter_email()

        customer.select_country()
        customer.save_customer()

        assert customer_name == CUSTOMER["name"]
        assert customer_email == CUSTOMER["email"]

        print("New Customer Created Successfully")