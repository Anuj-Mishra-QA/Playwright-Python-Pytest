from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.inventory_page import InventoryPage
from data.product_data import QUANTITY


def test_update_inventory(page):

    login = LoginPage(page)
    home = HomePage(page)
    inventory = InventoryPage(page)

    # Login
    login.login()

    # Navigate to Products
    home.open_sales()
    home.open_products()

    # Search Existing Product
    inventory.search_product()

    # Verify Track Inventory & Update Quantity
    inventory.verify_track_inventory()

    # Verify Updated Quantity
    quantity = inventory.verify_quantity_on_hand()

    # Validation
    assert float(quantity) == float(QUANTITY)