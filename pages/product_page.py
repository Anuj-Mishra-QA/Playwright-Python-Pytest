from datetime import datetime


class ProductPage:

    def __init__(self, page):
        self.page = page
        self.product_name = ""

    def create_product(self):

        # Click New
        self.page.get_by_role("button", name="New").click()
        print("New button clicked successfully")

        # Generate Product Name
        self.product_name = (
            "Automation_Product_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        # Enter Product Name
        product_name_field = self.page.get_by_placeholder("e.g. Cheese Burger")
        product_name_field.wait_for(state="visible")
        product_name_field.fill(self.product_name)

        print(f"Product Name Entered: {self.product_name}")

        # Product Details
        self.select_product_type("Goods")
        self.set_track_inventory(True)
        self.enter_price_details(100, 80)

        # Save
        self.save_product()

        return self.product_name

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