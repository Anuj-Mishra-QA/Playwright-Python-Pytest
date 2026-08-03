from data.purchase_data import VENDOR_NAME, PRODUCT_NAME, PURCHASE_ORDER_QUANTITY, UNIT_PRICE


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
        # quantity.press("Tab")

        print(f"Quotation Quantity Entered: {PURCHASE_ORDER_QUANTITY}")

    def unit_price(self):
        unit_price = self.page.locator("div[name='price_unit'] input")
        unit_price.wait_for(state="visible")
        unit_price.click()
        unit_price.fill(str(UNIT_PRICE))
        unit_price.press("Tab")

    def verify_tax_details(self):

        tax_locators = {
            "SGST/UTGST": self.page.locator("tr:has-text('SGST/UTGST') .o_tax_group_amount_value"),
            "CGST": self.page.locator("tr:has-text('CGST') .o_tax_group_amount_value"),
            "IGST": self.page.locator("tr:has-text('IGST') .o_tax_group_amount_value"),
            "Total": self.page.locator("span[name='amount_total']")
        }

        for tax_name, locator in tax_locators.items():

            if locator.count() > 0:
                value = locator.text_content().strip()
                print(f"{tax_name}: {value}")
            else:
                print(f"{tax_name}: Not Applicable (Skipped)")

    def confirm_order(self):
        self.page.get_by_role("button", name="Confirm Order").click()

    def receive_products(self):
        self.page.get_by_role("button", name="Receipt").click()
        self.page.get_by_role("button", name="Validate").click()
        self.page.wait_for_timeout(1000)
        breadcrumb = self.page.locator("li.o_back_button a")

        breadcrumb.wait_for(state="visible")
        breadcrumb.click()

        print("Returned to Purchase Order")

    def create_vendor_bill(self):
        ...