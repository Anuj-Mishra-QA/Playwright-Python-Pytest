from datetime import datetime


class CustomerPage:

    def __init__(self, page):
        self.page = page
        self.customer_name = ""
        self.customer_email = ""

    def new_customer(self):
        self.page.locator("button.o_list_button_add").click()

        print("New Customer opened")

        # Wait for Customer Name field
        self.page.locator("div[name='name'] input").wait_for(state="visible")

    def select_person(self):
        person_radio = self.page.locator("input[data-value='person']")

        person_radio.wait_for(state="visible")

        if not person_radio.is_checked():
            person_radio.check()

        print("Person selected")

    def enter_customer_name(self):

        self.customer_name = "Automation_Customer_" + datetime.now().strftime("%Y%m%d_%H%M%S")

        self.page.locator("input[id^='name']").fill(self.customer_name)

        print(f"Customer Name Entered: {self.customer_name}")

        print(f"Customer Name Entered: {self.customer_name}")

        return self.customer_name

    def enter_email(self):
        email = self.customer_name.lower() + "@gmail.com"

        self.page.locator("input[type='email']").fill(email)

        print(f"Email Entered: {email}")

        return email

    def verify_email(self):
        saved_email = self.page.locator("input[type='email']").input_value()

        print(f"Saved Email : {saved_email}")

        return saved_email

    def select_country(self, country):

        country_field = self.page.locator("input[id^='country_id']")

        country_field.click()
        country_field.fill(country)

        # Dropdown ka wait
        self.page.locator(".o-autocomplete--dropdown-menu").wait_for()

        # Exact country select
        self.page.locator(
            ".o-autocomplete--dropdown-menu .dropdown-item",
            has_text=country
        ).click()

        print(f"Country Selected: {country}")

    def save_customer(self):
        self.page.locator("i.fa-cloud-upload").click()
        print("Customer Saved Successfully")