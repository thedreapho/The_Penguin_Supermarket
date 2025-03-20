# __init__.py

"""
This module imports functions from the `funcs` module to make them available for use in the package.

By importing functions like `format_table`, `show_main_menu`, and others, this file serves as an entry
point for the operations of the Penguin SuperMarket program.

All functions related to displaying the menu, managing the inventory,
handling the shopping cart, and generating receipts are imported here.
"""

# Importing necessary functions from the `funcs` module
from .funcs import (
    format_table,               # Function to format and display data in a table format
    show_main_menu,             # Function to display the main menu to the user
    view_inventory,             # Function to show the current inventory
    view_your_cart,             # Function to show the user's shopping cart
    show_edit_menu,             # Function to display the menu for editing the cart
    add_product,                # Function to add products to the shopping cart
    quantity_edit,              # Function to edit the quantity of a product in the cart
    delete_product,             # Function to delete a product from the cart
    sort_products,              # Function to sort products in the cart
    create_receipt,             # Function to generate and display the receipt
    reset_inventory_and_cart,  # Function to reset the inventory and cart to their original state
    exit_program                # Function to exit the program and reset the system
)
