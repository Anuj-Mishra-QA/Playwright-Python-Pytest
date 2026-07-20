from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


def test_create_product(page):

    login = LoginPage(page)
    home = HomePage(page)
    product = ProductPage(page)

    # Login
    login.login()

    # Navigate to Products
    home.open_sales()
    home.open_products()

    # Create Product
    product_name = product.create_product()

    # Validation
    assert product_name.startswith("Automation_Product_")

    print(f"\nCreated Product : {product_name}")