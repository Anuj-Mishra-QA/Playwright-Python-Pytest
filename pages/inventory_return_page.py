import re
import pytest

from data.inventory_return_data import (
    SALES_ORDER_NUMBER,
    PRODUCT_NAME,
    RETURN_QUANTITY
)

from pages.home_page import HomePage


class InventoryReturnPage:

    def __init__(self, page):
        self.page = page

    # ---------------------------------------------------------
    # Step 1: Open Sales Order
    # ---------------------------------------------------------

    def open_sales_order(self):

        home = HomePage(self.page)

        # Go to Odoo home
        home.go_home()

        # Open Sales module
        home.open_sales()

        # Search Sales Order
        search_box = self.page.locator(
            "input.o_searchview_input"
        )

        search_box.wait_for(
            state="visible",
            timeout=30000
        )

        search_box.fill(SALES_ORDER_NUMBER)
        search_box.press("Enter")

        self.page.wait_for_timeout(1000)

        print(
            f"Searching Sales Order : "
            f"{SALES_ORDER_NUMBER}"
        )

        # Verify Sales Order exists
        so_record = self.page.get_by_role(
            "cell",
            name=SALES_ORDER_NUMBER,
            exact=True
        )

        if so_record.count() == 0:
            pytest.fail(
                f"Sales Order not available with this id: "
                f"{SALES_ORDER_NUMBER}"
            )

        so_record.first.wait_for(
            state="visible"
        )

        print(
            f"Sales Order Found : "
            f"{SALES_ORDER_NUMBER}"
        )

        # Open Sales Order
        so_record.first.click()

        print(
            f"Sales Order Opened : "
            f"{SALES_ORDER_NUMBER}"
        )

    # ---------------------------------------------------------
    # Step 2: Verify Product and Get Current On Hand Qty
    # ---------------------------------------------------------

    def verify_product_and_get_quantity(self):

        product_link = self.page.get_by_role(
            "link",
            name=PRODUCT_NAME,
            exact=True
        )

        if product_link.count() == 0:
            pytest.fail(
                f"Product are not available in order "
                f"with this name: {PRODUCT_NAME}"
            )

        product_link.first.click()

        print(
            f"Product Found in Order : "
            f"{PRODUCT_NAME}"
        )

        # Get On Hand Quantity
        on_hand_quantity = self.page.get_by_text(
            re.compile(r"On Hand")
        )

        on_hand_quantity.wait_for(
            state="visible"
        )

        # Click On Hand quantity area
        quantity_value = self.page.get_by_role(
            "main"
        ).get_by_text(
            re.compile(r"^\d+(?:\.\d+)?$")
        )

        if quantity_value.count() == 0:
            pytest.fail(
                f"On Hand Quantity not available "
                f"for product: {PRODUCT_NAME}"
            )

        current_quantity_text = (
            quantity_value.first.text_content().strip()
        )

        current_quantity = float(
            current_quantity_text.replace(",", "")
        )

        print(
            f"Current On Hand Quantity for "
            f"{PRODUCT_NAME}: {current_quantity}"
        )

        return current_quantity

    # ---------------------------------------------------------
    # Step 3: Return to Sales Order using Breadcrumb
    # ---------------------------------------------------------

    def return_to_sales_order(self):

        sales_order_link = self.page.locator(
            "ol"
        ).get_by_role(
            "link",
            name=SALES_ORDER_NUMBER,
            exact=True
        )

        sales_order_link.wait_for(
            state="visible"
        )

        sales_order_link.click()

        print(
            f"Returned to Sales Order : "
            f"{SALES_ORDER_NUMBER}"
        )

    # ---------------------------------------------------------
    # Step 4: Open Delivery
    # ---------------------------------------------------------

    def open_delivery(self):

        delivery_button = self.page.get_by_role(
            "button",
            name=re.compile(r"Delivery")
        )

        delivery_button.wait_for(
            state="visible"
        )

        delivery_button.click()

        print(
            "Delivery opened successfully"
        )

    # ---------------------------------------------------------
    # Step 5: Click Return
    # ---------------------------------------------------------

    def click_return(self):

        # ---------------------------------------------------------
        # Step 1: Find the Outgoing Delivery record
        # Example: WH/OUT/00231
        # ---------------------------------------------------------

        outgoing_transfer = self.page.locator(
            "td[name='name']"
        ).filter(
            has_text=re.compile(r"^WH/OUT/")
        ).first

        if outgoing_transfer.count() == 0:
            pytest.fail(
                f"Outgoing delivery record not available "
                f"for Sales Order: {SALES_ORDER_NUMBER}"
            )

        outgoing_transfer.wait_for(
            state="visible",
            timeout=30000
        )

        outgoing_reference = (
            outgoing_transfer.text_content()
            .strip()
        )

        print(
            f"Outgoing Delivery Found : "
            f"{outgoing_reference}"
        )

        # ---------------------------------------------------------
        # Step 2: Open the outgoing delivery
        # ---------------------------------------------------------

        outgoing_transfer.click()

        print(
            f"Outgoing Delivery Opened : "
            f"{outgoing_reference}"
        )

        # ---------------------------------------------------------
        # Step 3: Click Return button
        # ---------------------------------------------------------

        return_button = self.page.get_by_role(
            "button",
            name="Return",
            exact=True
        )

        return_button.wait_for(
            state="visible",
            timeout=30000
        )

        return_button.click()

        print(
            "Return button clicked"
        )

    # ---------------------------------------------------------
    # Step 6: Enter Return Quantity
    # ---------------------------------------------------------

    def enter_return_quantity(self):

        quantity_cell = self.page.get_by_role(
            "cell",
            name="0.00",
            exact=True
        )

        if quantity_cell.count() == 0:
            pytest.fail(
                "Return quantity field is not available"
            )

        quantity_cell.click()

        quantity_input = self.page.get_by_role(
            "textbox"
        )

        quantity_input.fill(
            str(RETURN_QUANTITY)
        )

        print(
            f"Return Quantity Entered : "
            f"{RETURN_QUANTITY}"
        )

    # ---------------------------------------------------------
    # Step 7: Create Return
    # ---------------------------------------------------------

    def create_return(self):

        return_button = self.page.locator(
            "button[name='action_create_returns']"
        )

        return_button.wait_for(
            state="visible"
        )

        return_button.click()

        print(
            "Return created successfully"
        )

    # ---------------------------------------------------------
    # Step 8: Validate Return
    # ---------------------------------------------------------

    def validate_return(self):

        validate_button = self.page.get_by_role(
            "button",
            name="Validate",
            exact=True
        )

        validate_button.wait_for(
            state="visible"
        )

        validate_button.click()

        print(
            "Return validated successfully"
        )

    # ---------------------------------------------------------
    # Step 9: Return to Sales Order
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    # Step 9: Return to Sales Order after Validation
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    # Step 9: Return to Sales Order after Validation
    # ---------------------------------------------------------

    def return_to_sales_order_after_validation(self):

        # -----------------------------------------------------
        # Step 9.1: Return page -> Original Delivery
        # -----------------------------------------------------

        outgoing_delivery_breadcrumb = (
            self.page.locator("ol.breadcrumb")
            .locator("a")
            .filter(has_text="WH/OUT/")
        )

        if outgoing_delivery_breadcrumb.count() == 0:
            pytest.fail(
                "Outgoing Delivery breadcrumb is not available "
                "after return validation"
            )

        outgoing_delivery_breadcrumb.first.wait_for(
            state="visible",
            timeout=30000
        )

        delivery_name = (
            outgoing_delivery_breadcrumb.first
            .text_content()
            .strip()
        )

        outgoing_delivery_breadcrumb.first.click()

        print(
            f"Returned to Original Delivery : "
            f"{delivery_name}"
        )

        self.page.wait_for_load_state(
            "domcontentloaded"
        )

        # -----------------------------------------------------
        # Step 9.2: Original Delivery -> Sales Order
        # -----------------------------------------------------

        sales_order_breadcrumb = (
            self.page.locator("ol.breadcrumb")
            .get_by_role(
                "link",
                name=SALES_ORDER_NUMBER,
                exact=True
            )
        )

        if sales_order_breadcrumb.count() == 0:
            pytest.fail(
                f"Sales Order breadcrumb not available "
                f"from delivery: {SALES_ORDER_NUMBER}"
            )

        sales_order_breadcrumb.first.wait_for(
            state="visible",
            timeout=30000
        )

        sales_order_breadcrumb.first.click()

        print(
            f"Returned to Sales Order after return validation : "
            f"{SALES_ORDER_NUMBER}"
        )

        self.page.wait_for_load_state(
            "domcontentloaded"
        )
    # ---------------------------------------------------------
    # Step 10: Open Product Again and Verify Quantity
    # ---------------------------------------------------------

    def verify_updated_quantity(self, previous_quantity):

        product_link = self.page.get_by_role(
            "link",
            name=PRODUCT_NAME,
            exact=True
        )

        if product_link.count() == 0:
            pytest.fail(
                f"Product are not available in order "
                f"with this name: {PRODUCT_NAME}"
            )

        product_link.first.click()

        print(
            f"Product Opened Again : "
            f"{PRODUCT_NAME}"
        )

        on_hand_quantity = self.page.get_by_text(
            re.compile(r"On Hand")
        )

        on_hand_quantity.wait_for(
            state="visible"
        )

        quantity_value = self.page.get_by_role(
            "main"
        ).get_by_text(
            re.compile(r"^\d+(?:\.\d+)?$")
        )

        if quantity_value.count() == 0:
            pytest.fail(
                f"Updated On Hand Quantity not available "
                f"for product: {PRODUCT_NAME}"
            )

        updated_quantity_text = (
            quantity_value.first.text_content().strip()
        )

        updated_quantity = float(
            updated_quantity_text.replace(",", "")
        )

        print(
            f"Updated On Hand Quantity for "
            f"{PRODUCT_NAME}: {updated_quantity}"
        )

        expected_quantity = (
            previous_quantity +
            float(RETURN_QUANTITY)
        )

        assert updated_quantity == expected_quantity, (
            f"On Hand Quantity was not increased correctly. "
            f"Previous Quantity: {previous_quantity}, "
            f"Return Quantity: {RETURN_QUANTITY}, "
            f"Expected Quantity: {expected_quantity}, "
            f"Actual Quantity: {updated_quantity}"
        )

        print(
            f"On Hand Quantity increased successfully: "
            f"{previous_quantity} -> {updated_quantity}"
        )

        return updated_quantity