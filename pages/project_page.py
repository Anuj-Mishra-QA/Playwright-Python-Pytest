import re
from datetime import datetime

from config import BASE_URL


class ProjectPage:
    def __init__(self, page):
        self.page = page

    def open_project_app(self):
        self.page.goto(f"{BASE_URL}/odoo")
        project_app = self.page.get_by_role("option", name="Project", exact=True)
        if project_app.count() and project_app.is_visible():
            project_app.click()
        else:
            self.page.goto(f"{BASE_URL}/odoo/project")
        self.page.locator(".o_control_panel").wait_for(state="visible")

    def new_project(self):
        list_view = self.page.get_by_role("button", name="List View")
        if list_view.count() and list_view.is_visible():
            list_view.click()

        new_button = self.page.get_by_role("button", name=re.compile(r"^New"))
        new_button.click()
        self.page.get_by_role("menuitem", name="New Project", exact=True).click()
        self.page.locator(".o_form_view").wait_for(state="visible")

    def enter_project_name(self, name):
        name_field = self.page.get_by_role("textbox", name="e.g. Office Party")
        name_field.wait_for(state="visible")
        name_field.fill(name)

    def select_project_manager(self, manager):
        manager_field = self.page.locator(
            ".o_form_view div[name='user_id'] input, "
            ".o_form_view div[name='user_ids'] input"
        ).first
        if not manager_field.count():
            manager_field = self.page.get_by_role(
                "combobox", name="Project Manager", exact=True
            )
        manager_field.wait_for(state="visible")
        manager_field.fill(manager)
        manager_option = self.page.get_by_role("option", name=manager, exact=True)
        manager_option.wait_for(state="visible", timeout=10000)
        manager_option.click()

    def _planned_date_inputs(self):
        start_field = self.page.locator(
            ".o_form_view input[id^='date_start']"
        ).first
        if start_field.count():
            # The end input is the third textbox in this form, as exposed by
            # the Odoo date-range widget and the recorded UI flow.
            return start_field, self.page.get_by_role("textbox").nth(2)

        named_inputs = self.page.get_by_role(
            "textbox", name=re.compile("Planned Date", re.IGNORECASE)
        )
        all_textboxes = self.page.get_by_role("textbox")
        if named_inputs.count() >= 2:
            return named_inputs.nth(0), named_inputs.nth(1)
        if named_inputs.count() == 1 and all_textboxes.count() >= 3:
            return named_inputs.first, all_textboxes.nth(2)
        raise AssertionError("Could not locate the project Planned Date fields")

    def enter_planned_dates(self, start_date, end_date):
        start_field, end_field = self._planned_date_inputs()
        for field, date_value in ((start_field, start_date), (end_field, end_date)):
            field.wait_for(state="visible")
            field.click()
            picker = self.page.locator(".o_datetime_picker")
            picker.wait_for(state="visible")
            header = picker.locator(".o_header_part").first
            target_month = date_value.strftime("%B %Y")

            for _ in range(24):
                current_month = header.inner_text().strip()
                if current_month == target_month:
                    break
                current = datetime.strptime(current_month, "%B %Y")
                target = datetime.strptime(target_month, "%B %Y")
                month_delta = (target.year - current.year) * 12 + target.month - current.month
                navigation = picker.locator(
                    "button.o_next" if month_delta > 0 else "button.o_previous"
                )
                navigation.click()
            else:
                raise AssertionError(f"Could not open calendar month {target_month}")

            day_cells = picker.locator(
                ".o_date_item_cell:not(.o_out_of_range)"
            )
            day_cell = None
            for index in range(day_cells.count()):
                candidate = day_cells.nth(index)
                if candidate.inner_text().strip() == str(date_value.day):
                    day_cell = candidate
                    break
            if day_cell is None:
                raise AssertionError(
                    f"Could not find day {date_value.day} in {target_month}"
                )
            day_cell.click()

    def enter_allocated_time(self, hours):
        allocated_time = self.page.get_by_role(
            "textbox", name="Allocated Time", exact=True
        )
        allocated_time.wait_for(state="visible")
        allocated_time.fill(str(hours))
        allocated_time.press("Tab")

    def save_project(self):
        save_button = self.page.get_by_role("button", name="Save manually")
        if save_button.count() and save_button.is_visible():
            save_button.click()
        else:
            save_button = self.page.locator(
                "button[title='Save manually'], button[name='save']"
            ).first
            save_button.wait_for(state="visible")
            save_button.click()
        self.page.locator(".o_form_view").wait_for(state="visible")

    def read_project_name(self, expected_name):
        title = self.page.get_by_text(expected_name, exact=True).last
        return title.inner_text().strip() if title.count() else ""
