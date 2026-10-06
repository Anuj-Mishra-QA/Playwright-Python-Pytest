import re
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config import BASE_URL


class CrmLeadStatePage:
    """Search CRM leads and verify or update their Won/Lost state."""

    STATE_ACTIONS = {
        "won": "button[name='action_set_won_rainbowman']",
        "lost": "button[title='Mark as lost'], button[title='Lost']",
    }

    def __init__(self, page):
        self.page = page
        self.rows = page.locator("tr.o_data_row")

    def open_crm(self):
        self.page.goto(f"{BASE_URL}/odoo/crm")
        self.page.locator(".o_content").wait_for(state="visible")

    def _use_list_view(self):
        list_view = self.page.locator(
            ".o_switch_view.o_list, button[aria-label='List'], button[title='List']"
        ).first
        if list_view.count() and list_view.is_visible():
            list_view.click()
        self.page.locator(".o_control_panel").wait_for(state="visible")

    def _matching_row_indexes(self, lead_name):
        indexes = []
        for index in range(self.rows.count()):
            row = self.rows.nth(index)
            name_cell = row.locator('td[name="name"], td[data-name="name"]').first
            if name_cell.count():
                row_name = name_cell.inner_text().strip()
            else:
                row_name = ""
                for cell in row.locator("td.o_data_cell").all():
                    cell_text = cell.inner_text().strip()
                    if cell_text.casefold() == lead_name.casefold():
                        row_name = cell_text
                        break
            if row_name.casefold() == lead_name.casefold():
                indexes.append(index)
        return indexes

    def search_leads(self, lead_name):
        self._use_list_view()
        search = self.page.locator("input.o_searchview_input").first
        search.wait_for(state="visible")
        search.fill(lead_name)
        search.press("Enter")
        self.page.locator(".o_control_panel").wait_for(state="visible")
        self.page.wait_for_timeout(500)
        return self._matching_row_indexes(lead_name)

    def search_lost_leads(self, lead_name):
        """Apply CRM's Lost filter to inspect archived lost leads too."""
        self.page.locator(".o_searchview_dropdown_toggler").first.click()
        lost_filter = self.page.get_by_role("menuitem", name="Lost", exact=True)
        if not lost_filter.count():
            lost_filter = self.page.locator(".o-dropdown--menu").get_by_text(
                "Lost", exact=True
            )
        lost_filter.wait_for(state="visible", timeout=10000)
        lost_filter.click()
        self.page.wait_for_timeout(500)
        return self._matching_row_indexes(lead_name)

    def open_result(self, row_index):
        row = self.rows.nth(row_index)
        name_cell = row.locator('td[name="name"], td[data-name="name"]').first
        if not name_cell.count():
            name_cell = row.locator("td.o_data_cell").first
        name_cell.click()
        self.page.locator(".o_form_view").wait_for(state="visible")
        match = re.search(r"/odoo/crm/(\d+)(?:[/?#]|$)", self.page.url)
        return match.group(1) if match else self.page.url

    def return_to_results(self):
        self.page.go_back(wait_until="domcontentloaded")
        self.page.locator(".o_control_panel").wait_for(state="visible", timeout=15000)
        self.page.wait_for_timeout(400)

    def _probability(self):
        field = self.page.locator(
            '.o_form_view .o_field_widget[name="probability"]'
        ).first
        if not field.count():
            field = self.page.locator('.o_form_view [name="probability"]').first
        if not field.count():
            return None
        input_field = field.locator("input").first
        raw_value = input_field.input_value() if input_field.count() else field.inner_text()
        match = re.search(r"\d+(?:\.\d+)?", raw_value)
        return float(match.group()) if match else None

    def is_in_state(self, state):
        target = state.casefold()
        ribbons = self.page.locator(".o_ribbon")
        for index in range(ribbons.count()):
            ribbon = ribbons.nth(index)
            if ribbon.is_visible() and ribbon.inner_text().strip().casefold() == target:
                return True
        if target == "won":
            return (self._probability() or 0) >= 100
        restore = self.page.get_by_role("button", name="Restore", exact=True)
        return restore.count() > 0 and restore.is_visible()

    def set_state(self, target_state, lost_reason=""):
        state = target_state.casefold()
        if state not in self.STATE_ACTIONS:
            raise ValueError("target_state must be 'Won' or 'Lost'")

        if state == "won":
            restore = self.page.get_by_role("button", name="Restore", exact=True)
            if restore.count() and restore.is_visible():
                restore.click()
                self.page.locator(self.STATE_ACTIONS["won"]).wait_for(
                    state="visible", timeout=15000
                )

        action = self.page.locator(self.STATE_ACTIONS[state]).first
        if state == "lost" and action.count() == 0:
            action = self.page.get_by_role("button", name="Lost", exact=True).first
        action.click()

        if state == "lost":
            dialog = self.page.get_by_role("dialog")
            try:
                dialog.wait_for(state="visible", timeout=10000)
            except PlaywrightTimeoutError:
                dialog = None
            if dialog:
                if lost_reason:
                    reason = dialog.get_by_role("combobox", name="Lost Reason")
                    if reason.count() and reason.is_visible():
                        reason.fill(lost_reason)
                        option = self.page.get_by_role("option", name=lost_reason, exact=True)
                        option.wait_for(state="visible", timeout=10000)
                        option.click()
                confirm = dialog.get_by_role("button", name="Mark as Lost", exact=True)
                if confirm.count() == 0:
                    confirm = dialog.get_by_role("button", name="Mark Lost", exact=True)
                if confirm.count() == 0:
                    confirm = dialog.get_by_role("button", name="Submit", exact=True)
                confirm.click()

        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if self.is_in_state(target_state):
                return
            self.page.wait_for_timeout(250)
        raise AssertionError(f"CRM lead did not reach {target_state} state")

    def current_stage(self):
        current = self.page.locator(
            ".o_form_view .o_statusbar_status .o_arrow_button_current, "
            ".o_form_view .o_statusbar_status button[aria-checked='true']"
        ).first
        if current.count():
            return current.inner_text().strip()
        return ""

    def set_stage(self, target_stage):
        """Move the open lead to a pipeline stage and wait for it to be selected."""
        if self.current_stage().casefold() == target_stage.casefold():
            return

        stage_button = self.page.locator(
            ".o_form_view .o_statusbar_status button"
        ).filter(has_text=target_stage).first
        if stage_button.count() == 0:
            stage_button = self.page.get_by_role(
                "button", name=target_stage, exact=True
            ).first
        stage_button.wait_for(state="visible", timeout=10000)
        stage_button.click()

        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if self.current_stage().casefold() == target_stage.casefold():
                return
            self.page.wait_for_timeout(250)
        raise AssertionError(f"CRM lead did not reach {target_stage} stage")
