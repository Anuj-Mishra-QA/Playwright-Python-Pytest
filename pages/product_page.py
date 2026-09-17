import re
from playwright.sync_api import expect
from data.product_data import PRODUCT_NAME, PRODUCT_QUANTITY, SALES_PRICE, COST_PRICE
from data.product_variant_data import IS_VARIANT, VARIANTS


class ProductPage:

    def __init__(self, page):
        self.page = page
        self.product_name = ""

    def create_product(self, product_name=None):
        if product_name:
            self.product_name = product_name
        else:
            self.product_name = PRODUCT_NAME

        if self.product_exists(self.product_name):
            self.open_existing_product(self.product_name)
            self.update_inventory_quantity(PRODUCT_QUANTITY)
            return self.product_name

        print("Product not found. Creating new product.")

        self.page.get_by_role("button", name="New").click()
        print("New button clicked successfully")

        product_name_field = self.page.get_by_placeholder(
            "e.g. Cheese Burger"
        )

        product_name_field.wait_for(state="visible")
        product_name_field.fill(self.product_name)

        print(f"Product Name Entered: {self.product_name}")

        self.select_product_type("Goods")
        self.set_track_inventory(True)
        self.enter_price_details(
            SALES_PRICE,
            COST_PRICE
        )

        if IS_VARIANT:
            self.handle_variant()

        self.save_product()
        self.update_inventory_quantity(PRODUCT_QUANTITY)

        return self.product_name

    def handle_variant(self):

        # Product type should be goods
        variant_tab = self.page.locator("a[name='variants']")

        if not variant_tab.is_visible():
            print("Attributes & Variants tab not available")
            return

        variant_tab.click()

        print("Attributes & Variants opened")

        for variant in VARIANTS:

            attribute = variant["attribute"]
            value = variant["value"]


            print(f"Processing Attribute : {attribute}")
            print(f"Processing Value : {value}")

            # Add Line
            self.page.locator(
                "td.o_field_x2many_list_row_add a"
            ).click()

            # Attribute Input
            attribute_input = self.page.locator(
                "td[name='attribute_id'] input.o-autocomplete--input"
            )

            attribute_input.fill(attribute)

            self.page.wait_for_timeout(1000)

            self.page.get_by_role(
                "option",
                name=attribute,
                exact=True
            ).click()

            print(f"Attribute Selected : {attribute}")
            # Value Field

            value_input = self.page.locator(
                "td[name='value_ids'] input.o-autocomplete--input"
            )

            value_input.wait_for(state="visible")

            value_input.click()

            value_input.fill(value)

            # Wait for dropdown

            self.page.locator(
                "ul.o-autocomplete--dropdown-menu"
            ).wait_for(state="visible")

            self.page.get_by_role(
                "option",
                name=value.capitalize(),
                exact=True
            ).click()

            print(f"Value Selected : {value}")

            print(f"Value Selected : {value}")

    def select_product_type(self, product_type):

        self.page.get_by_text(product_type, exact=True).click()

        print(f"Product Type Selected: {product_type}")

    def set_track_inventory(self, enable=True):

        checkbox = self.page.locator("input[id^='is_storable']")
        checkbox.wait_for(state="visible")

        if enable:
            if not checkbox.is_checked():
                checkbox.check()
            print("Track Inventory Enabled")
        else:
            if checkbox.is_checked():
                checkbox.uncheck()
            print("Track Inventory Disabled")

    def enter_price_details(self, sales_price, cost):

        sales_price_field = self.page.locator("input[id^='list_price']")
        sales_price_field.fill(str(sales_price))
        print(f"Sales Price Entered: {sales_price}")

        cost_field = self.page.locator("input[id^='standard_price']")
        cost_field.fill(str(cost))
        print(f"Cost Entered: {cost}")

    def save_product(self):

        save_button = self.page.locator("i.fa-cloud-upload")

        save_button.wait_for(state="visible")
        save_button.click()

        self.page.wait_for_timeout(2000)

        print("Product Saved Successfully")

    def product_exists(self, product_name):
        search_box = self.page.get_by_role(
            "searchbox",
            name="Search..."
        )

        search_box.wait_for(state="visible")
        search_box.fill(product_name)
        search_box.press("Enter")

        self.page.wait_for_timeout(1500)

        product_card = self.page.locator(
            ".o_kanban_record"
        ).filter(
            has=self.page.get_by_text(
                product_name,
                exact=True
            )
        )

        if product_card.count() > 0:
            print(f"Product already exists: {product_name}")
            return True

        print(f"Product does not exist: {product_name}")
        return False

    def open_existing_product(self, product_name):
        search_box = self.page.get_by_role(
            "searchbox",
            name="Search..."
        )

        search_box.wait_for(state="visible")
        search_box.fill(product_name)
        search_box.press("Enter")

        self.page.wait_for_timeout(1500)

        product_card = self.page.locator(
            ".o_kanban_record"
        ).filter(
            has=self.page.get_by_text(
                product_name,
                exact=True
            )
        ).first

        product_card.wait_for(state="visible")
        product_card.click()

        self.page.wait_for_timeout(1500)

        print(f"Existing Product Opened: {product_name}")

    def update_inventory_quantity(self, quantity):

        quantity_button = self.page.get_by_role(
            "button",
            name=re.compile(r"Units")
        )

        quantity_button.wait_for(state="visible")

        quantity_text = quantity_button.inner_text().strip()

        quantities = re.findall(
            r"\d+(?:\.\d+)?",
            quantity_text
        )

        if not quantities:
            raise ValueError(
                f"Unable to read current product quantity from: {quantity_text}"
            )

        current_quantity = float(quantities[0])

        print(f"Current Product Quantity Before Update: {current_quantity}")

        quantity_button.click()

        print("Quantity Details Opened")

        update_quantity_button = self.page.get_by_role(
            "button",
            name="Update Quantity"
        )

        update_quantity_button.wait_for(state="visible")
        update_quantity_button.click()

        print("Update Quantity opened")

        # Current quantity is 0
        if current_quantity == 0:

            print("Current Quantity is 0")
            print("Creating New Inventory Line")

            new_button = self.page.locator(
                "button.o_list_button_add"
            )

            new_button.wait_for(state="visible")
            new_button.click()

            print("New Inventory Line Created")

            quantity_input = self.page.get_by_role("textbox")
            quantity_input.wait_for(state="visible")
            quantity_input.fill(str(quantity))

            print(f"New Inventory Quantity Entered: {quantity}")

        # Current quantity is greater than 0
        else:

            print("Existing Product Quantity Found")

            quantity_cell = self.page.locator(
                "td[name='inventory_quantity_auto_apply']"
            ).first

            quantity_cell.wait_for(state="visible")
            quantity_cell.click(force=True)

            print("Existing Inventory Quantity Cell Opened")

            quantity_input = self.page.get_by_role("textbox")
            quantity_input.wait_for(state="visible")
            quantity_input.fill(str(quantity))

            print(f"Existing Inventory Quantity Updated: {quantity}")

        # Save
        self.page.get_by_role(
            "button",
            name="Save"
        ).click()

        print(f"Inventory Quantity Saved: {quantity}")

        self.page.wait_for_timeout(2000)

    def get_current_quantity(self):
        quantity_field = self.page.locator(
            "div[name='qty_available'].o_field_float"
        )

        quantity_field.wait_for(state="visible")

        quantity_text = quantity_field.inner_text().strip()

        current_quantity = float(quantity_text)

        print(f"Current Quantity : {current_quantity}")

        return current_quantity

    def get_sales_quantity(self):
        quantity_field = self.page.locator(
            "div[name='qty_available'].o_field_float.o_readonly_modifier"
        )

        quantity_field.wait_for(state="visible")

        quantity_text = quantity_field.inner_text().strip()

        current_quantity = float(quantity_text)

        print(f"Sales Current Quantity : {current_quantity}")

        return current_quantity