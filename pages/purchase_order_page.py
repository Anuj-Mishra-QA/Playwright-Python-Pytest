from data.purchase_data import VENDOR_NAME, PRODUCT_NAME, PURCHASE_ORDER_QUANTITY


class PurchasePage:


    def __init__(self, page):
        self.page = page

    def new_rfq(self):
        self.page.get_by_role("button", name="New").click()
        print("RFQ form view opened")

    def select_vendor(self):
        vendor = self.page.locator("#partner_id_0")
        vendor.click()
        vendor.fill(VENDOR_NAME)
        vendor.press("ArrowDown")
        vendor.press("Enter")
        print(f"Vendor Selected : {VENDOR_NAME}")

    def add_product(self):
        self.page.get_by_role("button", name="Add a product").click()

        product = self.page.get_by_role(
            "combobox",
            name="Search a product"
        )

        product.fill(PRODUCT_NAME)

        self.page.wait_for_timeout(1000)

        product.press("ArrowDown")
        product.press("Enter")

        print(f"Product Selected : {PRODUCT_NAME}")

    def enter_quantity(self):
        quantity= self.page.locator('div[name="product_qty"] input')
        quantity.wait_for(state="visible")
        quantity.click()
        quantity.fill(str(PURCHASE_ORDER_QUANTITY))
        quantity.press("Tab")

        print(f"Quotation Quantity Entered: {PURCHASE_ORDER_QUANTITY}")

    def confirm_order(self):
        ...

    def receive_products(self):
        ...

    def create_vendor_bill(self):
        ...