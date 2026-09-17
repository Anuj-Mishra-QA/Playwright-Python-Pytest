import pytest
import allure

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.purchase_order_page import PurchasePage

from data.purchase_data import (
    PRODUCT_NAME,
    PURCHASE_ORDER_QUANTITY,
    UNIT_PRICE
)


def test_purchase_order_flow(logged_in_page):

    home = HomePage(logged_in_page)
    product = ProductPage(logged_in_page)
    purchase = PurchasePage(logged_in_page)

def test_purchase_order_quantity_change(logged_in_page):
    home = HomePage(logged_in_page)
    product = ProductPage(logged_in_page)
    purchase = PurchasePage(logged_in_page)
    # --------------------------------------------------
    # Step 1: Check Initial Product Quantity
    # --------------------------------------------------

    home.go_home()
    home.open_purchase()

    logged_in_page.get_by_role(
        "button",
        name="Products",
        exact=True
    ).click()

    logged_in_page.get_by_role(
        "menuitem",
        name="Products"
    ).click()

    print("Products opened successfully")

    product.open_existing_product(PRODUCT_NAME)

    initial_quantity = product.get_current_quantity()

    print(f"Initial Product Quantity : {initial_quantity}")
    print(f"Purchase Order Quantity  : {PURCHASE_ORDER_QUANTITY}")

    with allure.step("Verify Initial Product Quantity"):
        allure.attach(
            f"Product Name        : {PRODUCT_NAME}\n"
            f"Previous Quantity   : {initial_quantity}\n"
            f"Purchase Quantity   : {PURCHASE_ORDER_QUANTITY}",
            name="Initial Product Stock",
            attachment_type=allure.attachment_type.TEXT
        )

    # --------------------------------------------------
    # Step 2: Create Purchase Order
    # --------------------------------------------------

    home.go_home()
    home.open_purchase()

    purchase.new_rfq()
    purchase.select_vendor()
    purchase.add_product()
    purchase.enter_quantity()
    purchase.unit_price()
    tax_details = purchase.verify_tax_details()

    with allure.step("Verify Purchase Order Amount"):
        allure.attach(
            f"Product Name : {PRODUCT_NAME}\n"
            f"Quantity     : {PURCHASE_ORDER_QUANTITY}\n"
            f"Unit Price   : {UNIT_PRICE}\n"
            f"{tax_details}",
            name="Purchase Order Amount Details",
            attachment_type=allure.attachment_type.TEXT
        )

    # --------------------------------------------------
    # Step 3: Confirm Purchase Order
    # --------------------------------------------------

    purchase.confirm_order()

    print("Purchase Order Confirmed Successfully")

    purchase_order_number = purchase.get_purchase_order_number()

    with allure.step("Purchase Order Details"):
        allure.attach(
            f"Purchase Order Number : {purchase_order_number}",
            name="Purchase Order ID",
            attachment_type=allure.attachment_type.TEXT
        )

    # --------------------------------------------------
    # Step 4: Receive Products
    # --------------------------------------------------

    purchase.receive_products()

    print("Products Received Successfully")

    # --------------------------------------------------
    # Step 5: Open Same Product from Purchase Order
    # --------------------------------------------------

    product_link = logged_in_page.locator(
        "a.o_form_uri[href*='/odoo/product.product/']"
    ).filter(
        has_text=PRODUCT_NAME
    )

    product_link.wait_for(state="visible")
    product_link.click()

    print(
        f"Product Opened from Purchase Order : "
        f"{PRODUCT_NAME}"
    )

    # --------------------------------------------------
    # Step 6: Check Updated Quantity
    # --------------------------------------------------

    updated_quantity = product.get_current_quantity()

    print(
        f"Updated Product Quantity : "
        f"{updated_quantity}"
    )

    # --------------------------------------------------
    # Step 7: Validate Quantity Addition
    # --------------------------------------------------

    expected_quantity = (
        initial_quantity +
        PURCHASE_ORDER_QUANTITY
    )

    print(
        f"Expected Product Quantity : "
        f"{expected_quantity}"
    )

    with allure.step("Validate Purchase Stock Addition"):
        allure.attach(
            f"Product Name              : {PRODUCT_NAME}\n"
            f"Previous Quantity         : {initial_quantity}\n"
            f"Purchase Order Quantity   : {PURCHASE_ORDER_QUANTITY}\n"
            f"Expected Current Quantity : {expected_quantity}\n"
            f"Actual Current Quantity   : {updated_quantity}\n"
            f"Quantity Added            : "
            f"{updated_quantity - initial_quantity}",
            name="Product Quantity Validation",
            attachment_type=allure.attachment_type.TEXT
        )

        assert updated_quantity == pytest.approx(
            expected_quantity,
            abs=0.01
        )

    # --------------------------------------------------
    # Step 8: Create Vendor Bill
    # --------------------------------------------------

    # Add your existing vendor bill flow here