import pytest


if __name__ == "__main__":

    pytest.main([
        "test/test_home.py",
        "test/test_customer.py",
        "test/test_product.py",
        "test/test_purchase_order.py",
        "test/test_purchase_bill.py",
        "test/test_quotation.py",
        "test/test_crm_lead.py",
        "test/test_crm_lead_state.py",
        "test/test_lead_to_quotation.py",
        "test/test_project.py",

        "--alluredir=reports/allure-result",
        "--clean-alluredir",

        "-v",
        "-s",

        "--html=reports/report.html",
        "--self-contained-html"
    ])
