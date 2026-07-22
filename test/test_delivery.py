from pages.home_page import HomePage
from pages.inventory_page import InventoryPage
from data.product_data import QUANTITY


def test_update_inventory(logged_in_page):

    home = HomePage(logged_in_page)
    inventory = InventoryPage(logged_in_page)

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