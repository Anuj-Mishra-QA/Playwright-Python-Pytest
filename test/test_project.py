import json
import random
from datetime import date, timedelta

import allure

from data.project_data import PROJECT
from pages.project_page import ProjectPage


@allure.feature("Project")
@allure.story("Create a project with randomized planning values")
@allure.title("Create a project with a data-driven manager and random dates/time")
def test_create_project_with_random_planning(logged_in_page):
    today = date.today()
    start_offset = random.randint(
        PROJECT["planned_start_days_ahead"],
        PROJECT["planned_start_window_days"],
    )
    planned_start = today + timedelta(days=start_offset)
    planned_end = planned_start + timedelta(
        days=random.randint(
            PROJECT["planned_duration_min_days"],
            PROJECT["planned_duration_max_days"],
        )
    )
    allocated_hours = random.randint(
        PROJECT["allocated_time_min"], PROJECT["allocated_time_max"]
    )

    project = ProjectPage(logged_in_page)
    allure.attach(
        json.dumps(
            {
                "project_name": PROJECT["name"],
                "project_manager": PROJECT["project_manager"],
                "planned_start": planned_start.isoformat(),
                "planned_end": planned_end.isoformat(),
                "allocated_hours": allocated_hours,
            },
            indent=2,
        ),
        name="Project creation data",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Open the Project app and start a new project"):
        project.open_project_app()
        project.new_project()

    with allure.step("Enter the project name and select its manager"):
        project.enter_project_name(PROJECT["name"])
        project.select_project_manager(PROJECT["project_manager"])

    with allure.step("Set a random planned date range and allocated time"):
        project.enter_planned_dates(planned_start, planned_end)
        project.enter_allocated_time(allocated_hours)

    with allure.step("Save and verify the project"):
        project.save_project()
        saved_name = project.read_project_name(PROJECT["name"])
        assert saved_name == PROJECT["name"], (
            f"Expected project '{PROJECT['name']}', got '{saved_name}'"
        )

    print(
        f"Created project '{saved_name}' with manager '{PROJECT['project_manager']}', "
        f"planned from {planned_start} to {planned_end}, "
        f"allocated {allocated_hours} hours."
    )
