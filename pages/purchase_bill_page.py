import os
import random
import pytest
from pathlib import Path
from data.purchase_bill_data import (
    PURCHASE_ORDER_NUMBER,
    BILL_DATE
)


class PurchaseBillPage:

    def __init__(self, page):
        self.page = page

    def search_purchase_order(self):
        search_box = self.page.locator(
            "input.o_searchview_input"
        )

        search_box.wait_for(state="visible")
        search_box.fill(PURCHASE_ORDER_NUMBER)
        search_box.press("Enter")

        self.page.wait_for_timeout(1000)

        print(
            f"Searching Purchase Order : "
            f"{PURCHASE_ORDER_NUMBER}"
        )

    def verify_purchase_order_exists(self):
        po_record = self.page.get_by_role(
            "cell",
            name=PURCHASE_ORDER_NUMBER,
            exact=True
        )

        if po_record.count() == 0:
            pytest.fail(
                "PO is not created with this reference number"
            )

        po_record.first.wait_for(state="visible")

        print(
            f"Purchase Order Found : "
            f"{PURCHASE_ORDER_NUMBER}"
        )

        return po_record.first

    def open_purchase_order(self):
        po_record = self.verify_purchase_order_exists()
        po_record.click()

        print(
            f"Purchase Order Opened : "
            f"{PURCHASE_ORDER_NUMBER}"
        )

    def set_bill_date(self):
        date_field = self.page.locator(
            "#invoice_date_1"
        )

        date_field.wait_for(state="visible")
        date_field.click()

        self.page.get_by_text(
            BILL_DATE,
            exact=True
        ).click()

        print(
            f"Bill Date Selected : "
            f"{BILL_DATE}"
        )

    def confirm_bill(self):
        self.page.get_by_role(
            "button",
            name="Confirm"
        ).click()

        print("Bill Confirmed Successfully")

    def verify_bill_amount(self):

        amount_locators = {
            "Untaxed Amount": self.page.locator(
                "span[name='Untaxed Amount']"
            ),
            "Tax": self.page.locator(
                "span.o_tax_group_amount_value"
            ),
            "Total": self.page.locator(
                "span[name='amount_total']"
            ),
            "Amount Due": self.page.get_by_text(
                "Amount Due"
            )
        }

        amount_details = []
        total_amount = None

        for amount_name, locator in amount_locators.items():

            if locator.count() > 0:

                if amount_name == "Amount Due":

                    value_locator = locator.locator(
                        "xpath=following::*[contains(@class, 'o_list_monetary')][1]"
                    )

                    if value_locator.count() > 0:
                        value = value_locator.first.text_content().strip()
                    else:
                        value = "Available"

                else:
                    value = locator.first.text_content().strip()

                print(
                    f"{amount_name}: {value}"
                )

                amount_details.append(
                    f"{amount_name}: {value}"
                )

                if amount_name == "Total":
                    total_amount = float(
                        value.replace("$", "")
                        .replace(",", "")
                        .strip()
                    )

            else:

                print(
                    f"{amount_name}: Not Applicable (Skipped)"
                )

                amount_details.append(
                    f"{amount_name}: Not Applicable (Skipped)"
                )

        assert total_amount is not None, (
            "Bill Total Amount could not be identified"
        )

        assert total_amount > 0, (
            f"No billable amount available for Purchase Order "
            f"{PURCHASE_ORDER_NUMBER}. "
            f"The PO may already be fully billed or have no "
            f"billable amount. "
            f"Current Bill Total: ${total_amount:.2f}"
        )

        return "\n".join(amount_details)

    def upload_bill(self):
        project_root = Path(__file__).resolve().parent.parent
        bill_file = project_root / "files" / "sample_bill.png"

        if not bill_file.exists():
            raise FileNotFoundError(
                f"Test bill file not found: {bill_file}"
            )

        with self.page.expect_file_chooser() as file_chooser_info:
            # Keep your existing Upload button locator here
            self.page.get_by_role(
                "button",
                name="Upload"
            ).click()

        file_chooser = file_chooser_info.value
        file_chooser.set_files(str(bill_file))

        return str(bill_file)

    def pay_bill(self):
        self.page.get_by_role(
            "button",
            name="Pay"
        ).click()

        print("Pay button clicked")

    def create_payment(self):
        self.page.get_by_role(
            "button",
            name="Create Payment"
        ).click()

        print("Payment Created Successfully")

    def return_to_purchase_order(self):
        purchase_order_link = self.page.locator(
            "ol"
        ).get_by_role(
            "link",
            name=PURCHASE_ORDER_NUMBER,
            exact=True
        )

        purchase_order_link.wait_for(state="visible")
        purchase_order_link.click()

        print(
            f"Returned to Purchase Order : "
            f"{PURCHASE_ORDER_NUMBER}"
        )