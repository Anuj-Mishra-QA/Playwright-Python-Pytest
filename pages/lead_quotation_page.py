import random

from config import BASE_URL


class LeadQuotationPage:
    """Open a random Won CRM lead and inspect its lead-created quotation."""

    def __init__(self, page):
        self.page = page
        self.rows = page.locator("tr.o_data_row")

    def _open_list_view(self):
        list_view = self.page.locator(
            ".o_switch_view.o_list, button[aria-label='List'], button[title='List']"
        ).first
        if list_view.count() and list_view.is_visible():
            list_view.click()
        self.page.locator(".o_control_panel").wait_for(state="visible")

    def _apply_won_filter(self):
        self.page.locator(".o_searchview_dropdown_toggler").first.click()
        won_filter = self.page.get_by_role("menuitem", name="Won", exact=True)
        if not won_filter.count():
            won_filter = self.page.locator(".o-dropdown--menu").get_by_text(
                "Won", exact=True
            )
        won_filter.wait_for(state="visible", timeout=10000)
        won_filter.click()
        self.page.locator(".o_control_panel").wait_for(state="visible")
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    @staticmethod
    def _cell_text(row, name):
        cell = row.locator(f'td[name="{name}"], td[data-name="{name}"]').first
        return cell.inner_text().strip() if cell.count() else ""

    def open_random_won_lead(self):
        self.page.goto(f"{BASE_URL}/odoo/crm")
        self.page.locator(".o_content").wait_for(state="visible")
        self._open_list_view()
        self._apply_won_filter()

        self.rows.first.wait_for(state="visible", timeout=15000)
        eligible = []
        for index in range(self.rows.count()):
            row = self.rows.nth(index)
            name = self._cell_text(row, "name")
            customer = ""
            for field_name in ("partner_id", "partner_name", "contact_name"):
                customer = self._cell_text(row, field_name)
                if customer and customer not in ("-", "/"):
                    break
            if name and customer:
                eligible.append((index, name, customer, row.inner_text().strip()))

        if not eligible:
            raise AssertionError("No Won CRM leads with a customer/contact were found")

        row_index, lead_name, row_customer, row_text = random.choice(eligible)
        row = self.rows.nth(row_index)
        name_cell = row.locator('td[name="name"], td[data-name="name"]').first
        name_cell.click()
        self.page.locator(".o_form_view").wait_for(state="visible")
        return {
            "lead_name": lead_name,
            "row_customer": row_customer,
            "row_text": row_text,
        }

    def _read_field(self, field_name, required=True):
        field = self.page.locator(
            f".o_form_view .o_field_widget[name='{field_name}']"
        ).first
        if not field.count():
            if required:
                raise AssertionError(f"Quotation field '{field_name}' was not found")
            return ""
        if not field.is_visible():
            if required:
                raise AssertionError(f"Quotation field '{field_name}' is not visible")
            return ""
        input_field = field.locator("input").first
        if input_field.count():
            value = input_field.input_value().strip()
            if value:
                return value
        return field.inner_text().strip()

    def read_lead_customer(self):
        for field_name in ("partner_id", "partner_name", "contact_name"):
            value = self._read_field(field_name, required=False)
            if value:
                return value
        return ""

    def click_new_quotation(self):
        lead_url = self.page.url
        button = self.page.locator(
            "button[name='action_sale_quotation_new']"
        ).first
        if not button.count():
            button = self.page.get_by_role(
                "button", name="New Quotation", exact=True
            ).first
        button.wait_for(state="visible", timeout=15000)
        button.click()
        self.page.wait_for_url(
            lambda url: url != lead_url,
            timeout=20000,
        )
        self.page.locator(".o_form_view").wait_for(state="visible", timeout=20000)
        self.page.locator(".o_form_view .o_field_widget[name='partner_invoice_id']").wait_for(
            state="visible", timeout=15000
        )

    def read_quotation_addresses(self):
        return {
            "customer": self._read_field("partner_id"),
            "invoice_address": self._read_field("partner_invoice_id"),
            "delivery_address": self._read_field("partner_shipping_id"),
        }

    def add_random_product(self):
        self.page.get_by_role("button", name="Add a product").click()
        product_input = self.page.get_by_role("combobox", name="Search a product")
        product_input.wait_for(state="visible")

        options = []
        for search_term in random.sample("abcdefghijklmnopqrstuvwxyz", 26):
            product_input.fill(search_term)
            self.page.wait_for_timeout(400)
            options = []
            for option in self.page.get_by_role("option").all():
                label = (option.inner_text() or "").strip()
                if (
                    option.is_visible()
                    and label
                    and "search more" not in label.casefold()
                    and not label.casefold().startswith("create ")
                ):
                    options.append((option, label))
            if options:
                break

        if not options:
            raise AssertionError("No selectable products appeared in the quotation")

        option, product_name = random.choice(options)
        option.click()

        confirm_variant = self.page.locator(
            "button[name='sale_product_configurator_confirm_button']"
        ).first
        if confirm_variant.count() and confirm_variant.is_visible():
            confirm_variant.click()
            self.page.locator(".o_technical_modal").wait_for(
                state="hidden", timeout=10000
            )

        self.page.locator("td[name='product_uom_qty']").last.wait_for(
            state="visible", timeout=15000
        )
        return product_name

    def set_unit_price(self, price):
        price_cell = self.page.locator("td[name='price_unit']").last
        price_cell.wait_for(state="visible", timeout=10000)
        price_cell.click()
        price_input = self.page.locator("div[name='price_unit'] input").last
        price_input.wait_for(state="visible", timeout=10000)
        price_input.fill(f"{price:.2f}")
        price_input.press("Tab")

    def save_quotation(self):
        save_button = self.page.get_by_role("button", name="Save manually")
        if save_button.count() and save_button.is_visible():
            save_button.click()
        else:
            save_button = self.page.locator("button[title='Save manually']")
            save_button.wait_for(state="visible", timeout=10000)
            save_button.click()
        self.page.locator(".o_form_view").wait_for(state="visible")
