from data.customer_data import CUSTOMER


class CustomerPage:

    def __init__(self, page):
        self.page = page
        self.customer_name = ""
        self.customer_email = ""

    def customer_exists_by_email(self, email):

        # Search customer using email
        search_box = self.page.locator(
            "input.o_searchview_input"
        )

        search_box.wait_for(state="visible")
        search_box.fill(email)
        search_box.press("Enter")

        self.page.wait_for_timeout(1000)

        # Check whether customer record exists
        customer_record = self.page.locator(
            ".o_data_row"
        ).filter(
            has_text=email
        )

        exists = customer_record.count() > 0

        print(f"Customer exists with email {email}: {exists}")

        return exists

    def new_customer(self):

        self.page.locator("button.o_list_button_add").click()

        print("New Customer opened")

        self.page.locator(
            "div[name='name'] input"
        ).wait_for(state="visible")

    def select_person(self):

        person_radio = self.page.locator(
            "input[data-value='person']"
        )

        person_radio.wait_for(state="visible")

        if not person_radio.is_checked():
            person_radio.check()

        print("Person selected")

    def enter_customer_name(self):

        self.customer_name = CUSTOMER["name"]

        self.page.locator(
            "input[id^='name']"
        ).fill(self.customer_name)

        print(
            f"Customer Name Entered: {self.customer_name}"
        )

        return self.customer_name

    def enter_email(self):

        self.customer_email = CUSTOMER["email"]

        self.page.locator(
            "input[type='email']"
        ).fill(self.customer_email)

        print(
            f"Email Entered: {self.customer_email}"
        )

        return self.customer_email

    def verify_email(self):

        saved_email = self.page.locator(
            "input[type='email']"
        ).input_value()

        print(f"Saved Email : {saved_email}")

        return saved_email

    def select_country(self):

        country = CUSTOMER["country"]

        country_field = self.page.locator(
            "input[id^='country_id']"
        )

        country_field.click()
        country_field.fill(country)

        self.page.locator(
            ".o-autocomplete--dropdown-menu"
        ).wait_for()

        self.page.locator(
            ".o-autocomplete--dropdown-menu .dropdown-item",
            has_text=country
        ).click()

        print(f"Country Selected: {country}")

    def save_customer(self):

        self.page.locator(
            "i.fa-cloud-upload"
        ).click()

        print("Customer Saved Successfully")

    def open_existing_customer(self, email):
        customer_record = self.page.locator(
            ".o_data_row"
        ).filter(
            has_text=email
        ).first

        customer_record.wait_for(state="visible")
        customer_record.click()

        print(f"Existing Customer Opened: {email}")

        self.page.locator(
            "div[name='name'] input"
        ).wait_for(state="visible")