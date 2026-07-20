from data.product_data import PRODUCT_NAME, QUANTITY


class InventoryPage:

    def __init__(self, page):
        self.page = page

    def search_product(self):
        # Search Product
        search_box = self.page.locator("input[placeholder='Search...']")

        search_box.wait_for(state="visible")
        search_box.fill(PRODUCT_NAME)
        search_box.press("Enter")

        print(f"Product Searched : {PRODUCT_NAME}")

        # Wait for search results
        self.page.wait_for_timeout(1500)

        # Locate Product Card
        product_card = self.page.locator(
            "article.o_kanban_record"
        ).filter(
            has_text=PRODUCT_NAME
        ).first

        product_card.wait_for(state="visible")
        product_card.scroll_into_view_if_needed()

        # Open Product Form
        product_card.click()

        print(f"Product Selected : {PRODUCT_NAME}")

        # Wait until URL changes to Product Form
        self.page.wait_for_url("**/odoo/products/*")

        # Wait for Track Inventory field (actual next step)
        self.page.locator("input[id^='is_storable']").wait_for(state="visible")

        print("Product Form View Opened Successfully")

    # from data.product_data import QUANTITY

    def verify_track_inventory(self):

        # Track Inventory Checkbox
        checkbox = self.page.locator("input[id^='is_storable']")

        checkbox.wait_for(state="visible")

        if checkbox.is_checked():
            print("Track Inventory is already enabled.")

        else:
            checkbox.check()
            print("Track Inventory Enabled Successfully.")

        # Quantity On Hand
        quantity_field = self.page.locator("div[name='qty_available'] input")

        quantity_field.wait_for(state="visible")
        quantity_field.click()
        quantity_field.fill(str(QUANTITY))
        quantity_field.press("Tab")

        print(f"Quantity Updated : {QUANTITY}")

    # def enter_inventory_quantity(self):
    #
    #     quantity_field = self.page.locator("input[id^='qty_available']")
    #
    #     quantity_field.wait_for(state="visible")
    #     quantity_field.click()
    #     quantity_field.fill(str(QUANTITY))
    #     quantity_field.press("Tab")

        print(f"Inventory Quantity Entered: {QUANTITY}")

    def verify_quantity_on_hand(self):

        quantity_field = self.page.locator("input[id^='qty_available']")

        quantity_field.wait_for(state="visible")

        current_quantity = quantity_field.input_value()

        print(f"Current Quantity On Hand: {current_quantity}")

        return current_quantity