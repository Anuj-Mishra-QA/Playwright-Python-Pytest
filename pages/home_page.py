class HomePage:

    def __init__(self, page):
        self.page = page

    def go_home(self):
        """
        Bring application to Odoo Home Dashboard.
        Called at the beginning of every test.
        """

        self.page.goto("https://edu-anujmishra.odoo.com/odoo")

        # Wait until top navigation is visible
        self.page.locator(".o_main_navbar").wait_for(timeout=30000)

        print("Home Dashboard opened successfully")

    def open_sales(self):

        self.page.get_by_text("Sales", exact=True).click()

        self.page.locator(".o_main_navbar").wait_for()

        print("Sales module opened successfully")

    def open_purchase(self):

        self.page.get_by_text("Purchase", exact=True).click()

        self.page.locator(".o_main_navbar").wait_for()

        print("Purchase module opened successfully")

    def open_products(self):
        self.page.get_by_text("Products", exact=True).click()

        self.page.get_by_text("Products", exact=True).nth(1).click()

        # Wait until Products page is loaded
        self.page.wait_for_url("**/odoo/products")

        print("Products opened successfully")

    def open_customers(self):

        self.page.get_by_text("Orders", exact=True).click()

        customers_menu = self.page.locator("a[href='/odoo/customers']")
        customers_menu.wait_for(state="visible")

        customers_menu.click()

        self.page.locator("button.o_list_button_add").wait_for()

        print("Customers opened successfully")

    def open_quotations(self):

        self.page.get_by_text("Orders", exact=True).click()

        self.page.get_by_text("Quotations", exact=True).click()

        self.page.locator("button.o_list_button_add").wait_for()

        print("Quotations opened successfully")