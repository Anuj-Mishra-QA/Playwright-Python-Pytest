import json

import allure

from data.crm_lead_data import CRM_LEAD
from data.crm_lead_state_data import LEAD_STATE_DATA
from pages.crm_lead_page import CrmLeadPage
from pages.crm_lead_state_page import CrmLeadStatePage


@allure.feature("CRM")
@allure.story("Create CRM leads and exercise states and pipeline stages")
@allure.title("Create leads for Won, Lost, Qualified, and Proposition")
def test_create_leads_and_apply_states_and_stages(logged_in_page):
    lost_reason = LEAD_STATE_DATA["lost_reason"]
    qualified_stage = LEAD_STATE_DATA["qualified_stage"]
    proposition_stage = LEAD_STATE_DATA["proposition_stage"]
    creator = CrmLeadPage(logged_in_page)
    state_page = CrmLeadStatePage(logged_in_page)

    test_data = {
        "lead": CRM_LEAD,
        "lost_reason": lost_reason,
        "qualified_stage": qualified_stage,
        "proposition_stage": proposition_stage,
    }
    allure.attach(
        json.dumps(test_data, indent=2),
        name="CRM lead workflow data",
        attachment_type=allure.attachment_type.JSON,
    )

    def create_and_open_lead(step_name):
        with allure.step(f"Create a new lead for {step_name}"):
            creator.open_crm()
            creator.create_new_lead()
            creator.enter_company(CRM_LEAD["company"])
            creator.enter_contact(CRM_LEAD["contact"])
            creator.enter_contact_email(CRM_LEAD["contact_email"])
            creator.add_lead()
            creator.open_created_opportunity(
                CRM_LEAD["company"], CRM_LEAD["contact"]
            )

    create_and_open_lead("Won")
    with allure.step("Mark the first new lead Won"):
        state_page.set_state("Won")
        assert state_page.is_in_state("Won"), "First new CRM lead did not reach Won"

    create_and_open_lead("Lost")
    with allure.step("Mark the second new lead Lost with its configured reason"):
        state_page.set_state("Lost", lost_reason)
        assert state_page.is_in_state("Lost"), "Second new CRM lead did not reach Lost"

    create_and_open_lead("Qualified and Proposition")
    with allure.step(f"Move the third new lead to {qualified_stage}"):
        state_page.set_stage(qualified_stage)
        assert state_page.current_stage().casefold() == qualified_stage.casefold()

    with allure.step(f"Move the third new lead to {proposition_stage}"):
        state_page.set_stage(proposition_stage)
        assert state_page.current_stage().casefold() == proposition_stage.casefold()

    message = (
        "Created three CRM leads: marked one Won, marked one Lost with reason "
        f"'{lost_reason}', and moved one through {qualified_stage} to {proposition_stage}."
    )
    print(message)
    allure.attach(
        message,
        name="Final CRM workflow assertion",
        attachment_type=allure.attachment_type.TEXT,
    )
