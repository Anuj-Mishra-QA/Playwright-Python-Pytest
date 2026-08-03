from pages.home_page import HomePage
from pages.inventory_page import InventoryPage
from data.product_data import QUANTITY


def test_update_inventory(logged_in_page):

    home = HomePage(logged_in_page)
    inventory = InventoryPage(logged_in_page)

    home.go_home()

    home.open_sales()
    home.open_products()

    inventory.search_product()

    inventory.verify_track_inventory()

    quantity = inventory.verify_quantity_on_hand()

    assert float(quantity) == float(QUANTITY)