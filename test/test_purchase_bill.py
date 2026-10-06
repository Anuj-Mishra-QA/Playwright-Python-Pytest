import allure

from pages.home_page import HomePage
from pages.purchase_bill_page import PurchaseBillPage

from data.purchase_bill_data import (
    PURCHASE_ORDER_NUMBER,
    BILL_DATE,
    BILL_FILE
)


def test_purchase_bill_flow(logged_in_page):

    home = HomePage(logged_in_page)
    purchase_bill = PurchaseBillPage(logged_in_page)

    # Step 1: Open Purchase
    home.go_home()
    home.open_purchase()

    # Step 2: Search Purchase Order
    purchase_bill.search_purchase_order()

    # Step 3: Verify and Open Purchase Order
    purchase_bill.open_purchase_order()

    # Step 4: Upload Bill
    bill_file = purchase_bill.upload_bill()

    # Step 5: Set Bill Date
    purchase_bill.set_bill_date()

    # Step 6: Confirm Bill
    purchase_bill.confirm_bill()

    # Step 7: Verify Bill Amount
    amount_details = purchase_bill.verify_bill_amount()

    with allure.step("Verify Purchase Bill Amount"):
        allure.attach(
            f"Purchase Order : {PURCHASE_ORDER_NUMBER}\n"
            f"Bill Date      : {BILL_DATE}\n"
            f"Bill Document  : {bill_file}\n"
            f"{amount_details}",
            name="Purchase Bill Amount Details",
            attachment_type=allure.attachment_type.TEXT
        )

    # Step 8: Pay Bill
    purchase_bill.pay_bill()

    # Step 9: Create Payment
    purchase_bill.create_payment()

    # Step 10: Return to Purchase Order
    purchase_bill.return_to_purchase_order()
