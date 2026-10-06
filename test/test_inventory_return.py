import allure

from pages.inventory_return_page import InventoryReturnPage

from data.inventory_return_data import (
    SALES_ORDER_NUMBER,
    PRODUCT_NAME,
    RETURN_QUANTITY
)


def test_inventory_return_flow(logged_in_page):

    inventory_return = InventoryReturnPage(
        logged_in_page
    )

    # ---------------------------------------------------------
    # Step 1: Search and open Sales Order
    # ---------------------------------------------------------

    inventory_return.open_sales_order()

    # ---------------------------------------------------------
    # Step 2: Open Product and get current On Hand Quantity
    # ---------------------------------------------------------

    current_quantity = (
        inventory_return
        .verify_product_and_get_quantity()
    )

    # ---------------------------------------------------------
    # Step 3: Return to Sales Order
    # ---------------------------------------------------------

    inventory_return.return_to_sales_order()

    # ---------------------------------------------------------
    # Step 4: Open Delivery
    # ---------------------------------------------------------

    inventory_return.open_delivery()

    # ---------------------------------------------------------
    # Step 5: Click Return
    # ---------------------------------------------------------

    inventory_return.click_return()

    # ---------------------------------------------------------
    # Step 6: Enter Return Quantity
    # ---------------------------------------------------------

    inventory_return.enter_return_quantity()

    # ---------------------------------------------------------
    # Step 7: Create Return
    # ---------------------------------------------------------

    inventory_return.create_return()

    # ---------------------------------------------------------
    # Step 8: Validate Return
    # ---------------------------------------------------------

    inventory_return.validate_return()

    # ---------------------------------------------------------
    # Step 9: Return to Sales Order
    # ---------------------------------------------------------

    inventory_return.return_to_sales_order_after_validation()

    # ---------------------------------------------------------
    # Step 10: Open Product Again and Verify Qty
    # ---------------------------------------------------------

    updated_quantity = (
        inventory_return
        .verify_updated_quantity(
            current_quantity
        )
    )

    # ---------------------------------------------------------
    # Allure Report
    # ---------------------------------------------------------

    with allure.step(
        "Verify Inventory Return Quantity"
    ):

        allure.attach(
            f"Sales Order       : {SALES_ORDER_NUMBER}\n"
            f"Product           : {PRODUCT_NAME}\n"
            f"Previous Quantity : {current_quantity}\n"
            f"Return Quantity   : {RETURN_QUANTITY}\n"
            f"Updated Quantity  : {updated_quantity}",
            name="Inventory Return Details",
            attachment_type=allure.attachment_type.TEXT
        )