from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config import BASE_URL


class CrmLeadPage:
    """Create a CRM opportunity, creating the company/contact when needed."""

    def __init__(self, page):
        self.page = page
        self.quick_create = page.locator(".o_kanban_quick_create").last

    def open_crm(self):
        self.page.goto(f"{BASE_URL}/odoo/crm")
        self.page.locator(".o_content").wait_for(state="visible")

    def opportunity_exists(self, company, contact):
        self.page.locator(".o_kanban_record").first.wait_for(state="visible", timeout=15000)
        matching_record = self.page.locator(".o_kanban_record").filter(
            has_text=company
        ).filter(has_text=contact)
        return matching_record.count() > 0
    def create_new_lead(self):
        self.page.get_by_role("button", name="New", exact=True).click()
        self.quick_create.wait_for(state="visible")

    def _fill_textbox(self, label, value):
        field = self.quick_create.get_by_role("combobox", name=label, exact=True)
        if field.count() == 0:
            field = self.quick_create.get_by_role("textbox", name=label, exact=True)
        field.wait_for(state="visible")
        field.fill(value)
        return field

    def _select_or_create(self, label, value):
        field = self._fill_textbox(label, value)
        create_option = self.page.get_by_role(
            "option", name=f'Create "{value}"', exact=True
        )
        existing_option = self.page.get_by_role("option", name=value, exact=True)

        try:
            create_option.wait_for(state="visible", timeout=2500)
            create_option.click()
        except PlaywrightTimeoutError:
            existing_option.wait_for(state="visible", timeout=10000)
            existing_option.click()

        # Wait for Odoo to accept the selected or newly-created relation.
        field.wait_for(state="visible")

    def enter_company(self, company):
        self._select_or_create("Company", company)

    def enter_contact(self, contact):
        self._select_or_create("Contact", contact)

    def enter_contact_email(self, email):
        self._fill_textbox("Contact Email", email)

    def add_lead(self):
        self.quick_create.get_by_role("button", name="Add", exact=True).click()

    def open_created_opportunity(self, company, contact):
        record = self.page.locator(".o_kanban_record").filter(
            has_text=company
        ).filter(has_text=contact).first
        record.wait_for(state="visible", timeout=15000)
        record.click()
        self.page.locator(".o_form_view").wait_for(state="visible")





