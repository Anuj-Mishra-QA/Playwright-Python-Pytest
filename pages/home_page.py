class HomePage:

    def __init__(self, page):
        self.page = page

    def open_sales(self):
        self.page.get_by_text("Sales", exact=True).click()
        print("Sales module opened successfully")

    def open_purchase(self):
        self.page.get_by_text("Purchase", exact=True).click()
        print("Purchase module opened successfully")

    def open_products(self):
        self.page.get_by_text("Products", exact=True).click()
        self.page.get_by_text("Products", exact=True).nth(1).click()
        print("Products opened successfully")

    def open_customers(self):
        # Orders menu
        self.page.get_by_text("Orders", exact=True).click()

        # Wait for Customers menu
        customers_menu = self.page.locator("a[href='/odoo/customers']")
        customers_menu.wait_for(state="visible")

        customers_menu.click()

        # Wait for Customers list page
        self.page.locator("button.o_list_button_add").wait_for(state="visible")

        print("Customers opened successfully")

    def open_quotations(self):
        self.page.get_by_text("Orders", exact=True).click()
        self.page.get_by_text("Quotations", exact=True).click()

        print("Quotations opened successfully")