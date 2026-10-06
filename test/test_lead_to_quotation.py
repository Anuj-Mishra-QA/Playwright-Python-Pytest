import json
import random

import allure

from pages.crm_lead_state_page import CrmLeadStatePage
from pages.lead_quotation_page import LeadQuotationPage
from pages.quotation_page import QuotationPage


@allure.feature("CRM to Sales")
@allure.story("Create a quotation from a Won lead")
@allure.title("Create a random draft quotation from a Won lead")
@allure.severity(allure.severity_level.NORMAL)
def test_create_quotation_from_random_won_lead(logged_in_page):
    lead_quotation = LeadQuotationPage(logged_in_page)
    with allure.step("Find and open a random Won lead with a customer"):
        lead = lead_quotation.open_random_won_lead()
        allure.dynamic.parameter("Won lead", lead["lead_name"])
        allure.attach(
            json.dumps(lead, indent=2),
            name="Selected Won lead",
            attachment_type=allure.attachment_type.JSON,
        )

    crm_state = CrmLeadStatePage(logged_in_page)
    with allure.step("Confirm the selected lead is Won"):
        assert crm_state.is_in_state("Won"), (
            f"Selected lead '{lead['lead_name']}' is not in Won state"
        )

    lead_customer = lead_quotation.read_lead_customer() or lead["row_customer"]
    assert lead_customer, f"Won lead '{lead['lead_name']}' has no customer"
    allure.attach(
        lead_customer,
        name="Customer on Won lead",
        attachment_type=allure.attachment_type.TEXT,
    )

    with allure.step("Open a quotation from the Won lead"):
        lead_quotation.click_new_quotation()

    with allure.step("Verify customer and addresses were carried into the quotation"):
        addresses = lead_quotation.read_quotation_addresses()
        assert addresses["customer"], "Quotation customer was not populated"
        assert addresses["customer"].casefold() == lead_customer.casefold(), (
            f"Quotation customer '{addresses['customer']}' does not match "
            f"lead customer '{lead_customer}'"
        )
        assert addresses["invoice_address"], "Quotation invoice address was not populated"
        assert addresses["delivery_address"], "Quotation delivery address was not populated"

    quotation = QuotationPage(logged_in_page)
    with allure.step("Select a random product and set random quantity and price"):
        product_name = lead_quotation.add_random_product()
        quantity = random.randint(1, 20)
        unit_price = round(random.uniform(10, 500), 2)
        quotation.enter_quantity(quantity)
        lead_quotation.set_unit_price(unit_price)
        allure.attach(
            json.dumps(
                {
                    "product": product_name,
                    "quantity": quantity,
                    "unit_price": unit_price,
                },
                indent=2,
            ),
            name="Random quotation line",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Check totals and save the draft quotation"):
        totals = quotation.verify_amount()
        lead_quotation.save_quotation()

    allure.attach(
        json.dumps(
            {
                "lead_name": lead["lead_name"],
                "lead_customer": lead_customer,
                **addresses,
                "product": product_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "quotation_totals": totals,
                "quotation_url": logged_in_page.url,
            },
            indent=2,
        ),
        name="Lead to quotation workflow summary",
        attachment_type=allure.attachment_type.JSON,
    )
