import pytest

pytest.main([
    "test/test_login.py",
    "test/test_home.py",
    "test/test_customer.py",
    "test/test_product.py",
    "test/test_delivery.py",
    "test/test_quotation.py",
    "test/test_purchase_order.py",

    "-v",
    "--html=reports/report.html",
    "--self-contained-html"
])