import pytest
import allure

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.quotation_page import QuotationPage

from data.quotation_data import (
    CUSTOMER_NAME,
    PRODUCT,
    SALES_ORDER_QUANTITY
)


def test_sales_quotation_flow(logged_in_page):

    home = HomePage(logged_in_page)
    product = ProductPage(logged_in_page)
    quotation = QuotationPage(logged_in_page)

    # --------------------------------------------------
    # Step 1: Check Initial Product Quantity
    # --------------------------------------------------

    home.go_home()
    home.open_sales()
    home.open_products()

    product_name = PRODUCT["name"]

    product.open_existing_product(product_name)

    initial_quantity = product.get_current_quantity()

    print(f"Initial Product Quantity : {initial_quantity}")
    print(f"Sales Order Quantity     : {SALES_ORDER_QUANTITY}")

    with allure.step("Verify Initial Product Quantity"):
        allure.attach(
            f"Product Name        : {product_name}\n"
            f"Initial Quantity    : {initial_quantity}\n"
            f"Sales Order Quantity: {SALES_ORDER_QUANTITY}",
            name="Initial Product Quantity",
            attachment_type=allure.attachment_type.TEXT
        )

    # --------------------------------------------------
    # Step 2: Create Quotation
    # --------------------------------------------------

    home.go_home()
    home.open_sales()

    quotation.new_quotation()
    quotation.select_customer()
    quotation.add_product(PRODUCT)
    quotation.enter_quantity(SALES_ORDER_QUANTITY)

    print(f"Quotation Created Product Selected: {product_name}")
    print(f"Quotation Quantity Entered: {SALES_ORDER_QUANTITY}")

    # --------------------------------------------------
    # Step 3: Verify Amount
    # --------------------------------------------------

    amount = quotation.verify_amount()

    with allure.step("Verify Quotation Amount"):
        allure.attach(
            f"Product Name  : {product_name}\n"
            f"Quantity      : {SALES_ORDER_QUANTITY}\n"
            f"Untaxed Amount: {amount['untaxed_amount']}\n"
            f"Tax           : {', '.join(amount['taxes'])}\n"
            f"Total Amount  : {amount['total']}",
            name="Quotation Amount",
            attachment_type=allure.attachment_type.TEXT
        )
    # --------------------------------------------------
    # Step 4: Confirm Sales Order
    # --------------------------------------------------

    quotation.confirm_order()

    print("Sales Order Confirmed Successfully")

    sales_order_number = quotation.get_sales_order_number()

    with allure.step("Sales Order Details"):
        allure.attach(
            f"Sales Order Number : {sales_order_number}",
            name="Sales Order ID",
            attachment_type=allure.attachment_type.TEXT
        )

    # --------------------------------------------------
    # Step 5: Open Delivery and Validate
    # --------------------------------------------------

    quotation.open_delivery()

    print("Delivery Opened Successfully")

    quotation.validate_delivery()

    print("Delivery Validated Successfully")

    # --------------------------------------------------
    # Step 6: Check Updated Product Quantity
    # --------------------------------------------------

    logged_in_page.get_by_role(
        "link",
        name=product_name,
        exact=True
    ).click()

    print("Product Opened")

    updated_quantity = product.get_sales_quantity()

    expected_quantity = (
        initial_quantity -
        SALES_ORDER_QUANTITY
    )

    print(f"Updated Product Quantity : {updated_quantity}")
    print(f"Expected Product Quantity : {expected_quantity}")

    with allure.step("Verify Updated Product Quantity"):
        allure.attach(
            f"Product Name       : {product_name}\n"
            f"Initial Quantity   : {initial_quantity}\n"
            f"Sales Order Quantity: {SALES_ORDER_QUANTITY}\n"
            f"Updated Quantity   : {updated_quantity}\n"
            f"Expected Quantity  : {expected_quantity}",
            name="Updated Product Quantity",
            attachment_type=allure.attachment_type.TEXT
        )

    assert updated_quantity == pytest.approx(
        expected_quantity,
        abs=0.01
    )

    # --------------------------------------------------
    # Step 7: Return to Sales Order
    # --------------------------------------------------

    logged_in_page.go_back()
    logged_in_page.wait_for_timeout(1500)

    print("Returned to Sales Order Form View")

    # --------------------------------------------------
    # Step 8: Create Invoice
    # --------------------------------------------------

    quotation.create_regular_invoice()

    print("Create Invoice")
    print("Create Draft")
    print("Confirm Invoice")