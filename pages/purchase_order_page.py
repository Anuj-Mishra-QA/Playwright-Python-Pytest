import re
from playwright.sync_api import TimeoutError
from data.purchase_data import (
    VENDOR_NAME,
    PRODUCT_NAME,
    PURCHASE_ORDER_QUANTITY,
    UNIT_PRICE
)

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

        product = self.page.get_by_role("combobox", name="Search a product")
        product.fill(PRODUCT_NAME)

        option = self.page.get_by_role("option", name=PRODUCT_NAME, exact=True)
        option.wait_for(state="visible", timeout=5000)
        option.click()

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
            "Untaxed Amount": self.page.locator(
                "span[name='Untaxed Amount']"
            ),
            "SGST/UTGST": self.page.locator(
                "tr:has-text('SGST/UTGST') .o_tax_group_amount_value"
            ),
            "CGST": self.page.locator(
                "tr:has-text('CGST') .o_tax_group_amount_value"
            ),

            "Tax": self.page.locator(
                "span.o_tax_group_amount_value"
            ),

            "IGST": self.page.locator(
                "tr:has-text('IGST') .o_tax_group_amount_value"
            ),
            "Total": self.page.locator(
                "span[name='amount_total']"
            )
        }

        tax_details = []

        for tax_name, locator in tax_locators.items():

            if locator.count() > 0:
                value = locator.text_content().strip()
                print(f"{tax_name}: {value}")
                tax_details.append(f"{tax_name}: {value}")
            else:
                print(f"{tax_name}: Not Applicable (Skipped)")
                tax_details.append(
                    f"{tax_name}: Not Applicable (Skipped)"
                )

        return "\n".join(tax_details)

    def confirm_order(self):
        self.page.get_by_role("button", name="Confirm Order").click()

    def receive_products(self):
        self.page.get_by_role("button", name="Receipt").click()

        validate_btn = self.page.get_by_role("button", name="Validate")
        validate_btn.wait_for(state="visible")
        validate_btn.click()

        try:
            alert = self.page.get_by_text("Transfer trouble alert!")
            alert.wait_for(state="visible", timeout=3000)

            print("\n===== ALERT MESSAGE =====")
            print(alert.text_content().strip())

            self.page.locator(
                "footer.modal-footer button.o-default-button"
            ).click()

            demand_qty = self.page.locator(
                "td[name='product_qty']"
            ).text_content().strip()

            print(f"Demand Quantity : {demand_qty}")

            quantity_cell = self.page.locator("td[name='quantity']")
            quantity_cell.click()

            quantity_input = self.page.locator("td[name='quantity'] input")
            quantity_input.fill(demand_qty)

            print(f"Entered Quantity : {demand_qty}")

            validate_btn.click()

        except TimeoutError:
            print("No Alert Displayed")

        self.page.wait_for_timeout(1000)

        breadcrumb = self.page.locator("li.o_back_button a")
        breadcrumb.wait_for(state="visible")
        breadcrumb.click()

        print("Returned to Purchase Order")

    def create_vendor_bill(self, bill_file):
        self.page.get_by_role(
            "button",
            name="Upload Bill"
        ).click()

        self.page.get_by_role(
            "button",
            name="Upload Bill"
        ).set_input_files(bill_file)

        print("Vendor Bill Uploaded")

        self.page.get_by_role(
            "button",
            name="Confirm"
        ).click()

        print("Vendor Bill Confirmed")

        self.page.get_by_text("Close").click()

        print("Vendor Bill Closed")

        self.page.locator("#invoice_date_1").click()

        self.page.get_by_text("16").click()

        self.page.get_by_role(
            "button",
            name="Save manually"
        ).click()

        self.page.get_by_role(
            "button",
            name="Confirm"
        ).click()

        print("Vendor Bill Date Confirmed")

    def get_current_quantity(self):
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

        print(f"Current Quantity : {current_quantity}")

        return current_quantity

    def wait_for_backend_update(self, seconds):
        print(f"Waiting {seconds} seconds for backend quantity update...")
        self.page.wait_for_timeout(seconds * 1000)

    def get_purchase_order_number(self):

        order_number = self.page.locator(
            "div[name='name'] span"
        ).inner_text().strip()

        print(f"Purchase Order Number : {order_number}")

        return order_number