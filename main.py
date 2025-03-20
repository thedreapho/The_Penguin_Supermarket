import warnings
import pandas as pd
from tools import(
    format_table,
    show_main_menu,
    view_inventory,
    view_your_cart,
    show_edit_menu,
    add_product,
    quantity_edit,
    delete_product,
    sort_products,
    create_receipt,
    reset_inventory_and_cart,
    exit_program
)



warnings.simplefilter(action='ignore', category=FutureWarning)

print("\n--> Welcome To The Penguin SuperMarket! <--")
show_main_menu()