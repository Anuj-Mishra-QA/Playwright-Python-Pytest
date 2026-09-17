import allure

from pages.home_page import HomePage
from pages.product_page import ProductPage


def test_create_product(logged_in_page):

    home = HomePage(logged_in_page)
    product = ProductPage(logged_in_page)

    home.go_home()
    home.open_sales()
    home.open_products()

    with allure.step("Create Product"):

        product_name = product.create_product()

        allure.attach(
            f"Product Name : {product_name}",
            name="Created Product",
            attachment_type=allure.attachment_type.TEXT
        )

    print(f"Product Created/Verified : {product_name}")