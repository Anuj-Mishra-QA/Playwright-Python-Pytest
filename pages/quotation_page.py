from playwright.sync_api import TimeoutError
from data.quotation_data import (
    CUSTOMER_NAME,
    PRODUCT,
    SALES_ORDER_QUANTITY,
)


class QuotationPage:

    def __init__(self, page):
        self.page = page

    def new_quotation(self):

        self.page.get_by_text("Orders", exact=True).click()
        self.page.get_by_role("menuitem", name="Quotations").click()

        print("Quotations opened successfully")

        self.page.get_by_role("button", name="New").click()

        print("New Quotation opened")

    def select_customer(self):

        customer_field = self.page.locator("input[id^='partner_id']")

        customer_field.wait_for(state="visible")
        customer_field.click()
        customer_field.fill(CUSTOMER_NAME)

        self.page.wait_for_timeout(1000)

        customer_field.press("ArrowDown")
        customer_field.press("Enter")

        print(f"Customer Selected : {CUSTOMER_NAME}")

    def add_product(self, product):
        self.page.get_by_role(
            "button",
            name="Add a product"
        ).click()

        product_field = self.page.get_by_role(
            "combobox",
            name="Search a product"
        )

        product_field.fill(product["name"])
        self.page.wait_for_timeout(1000)

        product_option = self.page.get_by_role(
            "option",
            name=product["name"],
            exact=True
        ).first

        product_option.wait_for(state="visible")
        product_option.click()

        print(f"Product Selected : {product['name']}")

        attributes = product.get("attributes", {})

        if attributes:
            # Attribute/Variant selection yahan handle hoga
            ...

    def handle_variant(self):

        print("Variant Configurator Opened")

        for attribute, value in PRODUCT["attributes"].items():
            print(f"Selecting {attribute} : {value}")

            self.page.get_by_text(
                value,
                exact=True
            ).click()

        confirm_btn = self.page.locator(
            "button[name='sale_product_configurator_confirm_button']"
        )

        confirm_btn.wait_for(state="visible")
        confirm_btn.click()

        # Variant popup close hone ka wait
        self.page.locator("div.o_technical_modal").wait_for(
            state="hidden",
            timeout=10000
        )

        # Quotation line load hone ka wait
        self.page.wait_for_load_state("domcontentloaded")

        # Product row visible hone ka wait
        self.page.locator(
            "td[name='product_uom_qty']"
        ).wait_for(
            state="visible",
            timeout=10000
        )

        print("Variant Confirmed Successfully")

    def enter_quantity(self, quantity):

        quantity_cell = self.page.locator(
            "td[name='product_uom_qty']"
        )

        quantity_cell.wait_for(state="visible")
        quantity_cell.click()

        quantity_input = self.page.locator(
            "div[name='product_uom_qty'] input"
        )

        quantity_input.wait_for(state="visible")
        quantity_input.fill(str(quantity))
        quantity_input.press("Tab")

        print(f"Quotation Quantity Entered: {quantity}")

    def verify_amount(self):

        # Wait for Total Amount
        self.page.locator("span[name='amount_total']").wait_for(state="visible")

        untaxed_amount = self.page.locator(
            "span[name='Untaxed Amount']"
        ).inner_text().strip()

        total_amount = self.page.locator(
            "span[name='amount_total']"
        ).inner_text().strip()

        tax_values = self.page.locator("span.o_tax_group_amount_value")

        taxes = []

        for i in range(tax_values.count()):
            taxes.append(tax_values.nth(i).inner_text().strip())

        print("\n===== Amount Details =====")
        print(f"Untaxed Amount : {untaxed_amount}")

        if taxes:
            for index, tax in enumerate(taxes, start=1):
                print(f"Tax {index} : {tax}")
        else:
            print("Tax : Not Available")

        print(f"Total Amount : {total_amount}")

        return {
            "untaxed_amount": untaxed_amount,
            "taxes": taxes,
            "total": total_amount
        }

    def confirm_order(self):

        self.page.get_by_role(
            "button",
            name="Confirm"
        ).click()

        print("Sales Order Confirmed Successfully")

    def open_delivery(self):

        delivery_btn = self.page.locator(
            "button:has(i.fa-truck)"
        )

        delivery_btn.wait_for(state="visible")
        delivery_btn.click()

        print("Delivery Opened Successfully")

    def validate_delivery(self):

        validate_btn = self.page.locator(
            "button[name='button_validate']"
        )

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

            print("Alert Closed Successfully")

            demand_qty = self.page.locator(
                "td[name='product_uom_qty']"
            ).text_content().strip()

            print(f"Demand Quantity : {demand_qty}")

            quantity_cell = self.page.locator(
                "td[name='quantity']"
            )

            quantity_cell.click()

            quantity_input = self.page.locator(
                "td[name='quantity'] input"
            )

            quantity_input.fill(demand_qty)

            print(f"Entered Quantity : {demand_qty}")

            validate_btn.click()

        except TimeoutError:
            print("No Alert Displayed")

        print("Delivery Validated Successfully")

        breadcrumb = self.page.locator("li.o_back_button a")
        breadcrumb.wait_for(state="visible")
        breadcrumb.click()

        print("Returned to Sales Order")

    def create_regular_invoice(self):

        self.page.get_by_role(
            "button",
            name="Create Invoice"
        ).click()

        print("Create Invoice Clicked")

        self.page.get_by_role(
            "button",
            name="Create Draft"
        ).click()

        print("Draft Invoice Created")

        self.page.get_by_role(
            "button",
            name="Confirm"
        ).click()

        print("Invoice Confirmed Successfully")

    def get_sales_order_number(self):

        order_number = self.page.locator(
            "div[name='name'] span"
        ).inner_text().strip()

        print(f"Sales Order Number : {order_number}")

        return order_number