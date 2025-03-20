# Importing the warnings module to manage warning messages in the program
import warnings

# Importing pandas as pd for data manipulation (if needed later in the program)
import pandas as pd

# Importing various functions from the 'tools' module to handle various functionalities
from tools import (
    format_table,         # Function to format and display tables
    show_main_menu,       # Function to display the main menu of the supermarket
    view_inventory,       # Function to view the current inventory of products
    view_your_cart,       # Function to view the user's shopping cart
    show_edit_menu,       # Function to display options for editing the cart or inventory
    add_product,          # Function to add a new product to the inventory
    quantity_edit,        # Function to edit the quantity of a product in the inventory or cart
    delete_product,       # Function to delete a product from the cart or inventory
    sort_products,        # Function to sort products based on name, price, or quantity
    create_receipt,       # Function to generate a receipt for the purchased items
    reset_inventory_and_cart,  # Function to reset both inventory and cart (clear them)
    exit_program          # Function to exit the program
)

# Configuring warnings to ignore future warnings (useful for avoiding unnecessary warning messages)
warnings.simplefilter(action='ignore', category=FutureWarning)

# Main greeting message to the user when they start the program
print("\n--> Welcome To The Penguin SuperMarket! <--")

# Calling the function to display the main menu of the supermarket
show_main_menu()
