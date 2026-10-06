import json

import allure

from pages.crm_lead_page import CrmLeadPage
from data.crm_lead_data import CRM_LEAD


@allure.feature("CRM")
@allure.story("Create opportunity with company and contact")
@allure.title("Create CRM opportunity using company and contact data")
def test_create_crm_lead(logged_in_page):
    # logged_in_page uses LoginPage, which reads USERNAME and PASSWORD from config.py.
    crm = CrmLeadPage(logged_in_page)
    allure.attach(
        json.dumps(CRM_LEAD, indent=2),
        name="CRM lead test data",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Open the Odoo CRM module"):
        crm.open_crm()

    with allure.step("Check whether the CRM details already exist"):
        if crm.opportunity_exists(CRM_LEAD["company"], CRM_LEAD["contact"]):
            message = (
                "CRM details are already created for "
                f"Company: {CRM_LEAD['company']}, "
                f"Contact: {CRM_LEAD['contact']}. "
                f"Contact Email in data: {CRM_LEAD['contact_email']}. "
                "Skipping duplicate lead creation."
            )
            print(message)
            allure.attach(
                message,
                name="Existing CRM details",
                attachment_type=allure.attachment_type.TEXT,
            )
            return

    with allure.step("Start a new CRM opportunity"):
        crm.create_new_lead()

    with allure.step("Select or create the company"):
        crm.enter_company(CRM_LEAD["company"])

    with allure.step("Select or create the contact"):
        crm.enter_contact(CRM_LEAD["contact"])

    with allure.step("Enter the contact email"):
        crm.enter_contact_email(CRM_LEAD["contact_email"])

    with allure.step("Add the opportunity"):
        crm.add_lead()

    with allure.step("Open the newly created opportunity"):
        crm.open_created_opportunity(
            CRM_LEAD["company"], CRM_LEAD["contact"]
        )
