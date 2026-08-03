from pages.home_page import HomePage
from pages.product_page import ProductPage


def test_create_product(logged_in_page):

    home = HomePage(logged_in_page)
    product = ProductPage(logged_in_page)

    home.go_home()

    home.open_sales()
    home.open_products()

    product_name = product.create_product()

    assert product_name.startswith("Automation_Product_")

    print(f"\nCreated Product : {product_name}")