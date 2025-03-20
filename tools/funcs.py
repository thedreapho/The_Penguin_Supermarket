import pandas as pd
import shutil

inventory_file_path = 'D:\Coding\my codings\AllOfTheCodes\Final project\database\penguin_sm_inventory.csv'
customer_cart_file_path = 'D:\Coding\my codings\AllOfTheCodes\Final project\database\customer_cart.csv'
final_receipt_file_path = r'D:\Coding\my codings\AllOfTheCodes\Final project\database\final_receipt.csv'

original_inventory = 'D:\Coding\my codings\AllOfTheCodes\Final project\database\original_inventory.csv'
original_cart = 'D:\Coding\my codings\AllOfTheCodes\Final project\database\original_cart.csv'
original_receipt = 'D:\Coding\my codings\AllOfTheCodes\Final project\database\original_receipt.csv'


# --------------------------------------------------------
def format_table(df):
    # Get the column names and data
    columns = df.columns
    data = df.values
    if df.empty:
        print("Your cart is empty.")
        return

    # Calculate column widths for alignment
    column_widths = [max(len(str(val)) for val in df[col]) for col in columns]
    column_widths = [max(width, len(col)) for width, col in zip(column_widths, columns)]  # Ensure the header fits

    # Create top border
    border = "+".join(["-" * (width + 2) for width in column_widths])
    print(f"+{border}+")

    # Print headers
    header_row = " | ".join([col.ljust(width) for col, width in zip(columns, column_widths)])
    print(f"| {header_row} |")

    # Print separator line between header and data
    print(f"+{border}+")

    # Print each row of the data
    for row in data:
        if row[0] == 'TOTAL':
            print(f"+{border}+")

        formatted_row = " | ".join([str(val).ljust(width) for val, width in zip(row, column_widths)])
        print(f"| {formatted_row} |")

    # Print bottom border
    print(f"+{border}+")


def show_main_menu():
    menu_data = {
        'Option': [1, 2, 3, 4, 5],
        'Action': [
            'View inventory',
            'View your cart',
            'Edit your cart',
            'Create receipt',
            'Exit'
        ]
    }
    menu_df = pd.DataFrame(menu_data)

    while True:
        # Display the menu
        print("\nMain Menu:")
        format_table(menu_df)

        # Get the user's choice
        choice = int(input("Please choose an option (1-5): "))

        # Find the right action
        if choice in menu_df['Option'].values:
            action = menu_df.loc[menu_df['Option'] == choice, 'Action'].values[0]
            print(f"You selected: {action}")

            # Matching the action with the user's choice
            if action == 'View inventory':
                view_inventory()
            elif action == 'View your cart':
                view_your_cart()
            elif action == 'Add a product to your cart':
                add_product()
            elif action == 'Edit your cart':
                show_edit_menu()
            elif action == 'Create receipt':
                create_receipt()
            elif action == 'Exit':
                exit_program()
            else:
                print("Invalid choice. Please try again.")


def view_inventory():
    inventory_df = pd.read_csv(inventory_file_path)
    format_table(inventory_df)


def view_your_cart():
    cart_df = pd.read_csv(customer_cart_file_path)
    format_table(cart_df)


def show_edit_menu():
    edit_menu_data = {
        'Option': [1, 2, 3, 4, 5],
        'Action': [
            'Add a product to your cart',
            'Edit the quantity of a item',
            'Sort products in your cart',
            'Delete an item from your cart permanently',
            'Back to MainMenu!'
        ]
    }
    edit_menu_df = pd.DataFrame(edit_menu_data)

    while True:
        # Display the menu
        print("\nEdit Menu:")
        format_table(edit_menu_df)

        # Get the user's choice
        choice = int(input("Please choose an option (1-5): "))

        # Find the right action
        if choice in edit_menu_df['Option'].values:
            action = edit_menu_df.loc[edit_menu_df['Option'] == choice, 'Action'].values[0]
            print(f"You selected: {action}")

            # Matching the action with the user's choice
            if action == 'Add a product to your cart':
                add_product()
            elif action == 'Edit the quantity of a item':
                quantity_edit()
            elif action == 'Sort products in your cart':
                sort_products()
            elif action == 'Delete an item from your cart permanently':
                delete_product()
            elif action == 'Create the final receipt from all of the items in your cart':
                create_receipt()
            elif action == 'Back to MainMenu!':
                show_main_menu()
            else:
                print("Invalid choice. Please try again.")


def add_product():
    inventory_df = pd.read_csv(inventory_file_path)
    cart_df = pd.read_csv(customer_cart_file_path)

    new_item = input("Enter your item: ").strip().capitalize()
    if new_item not in inventory_df['Product'].str.capitalize().values:
        print(f"'{new_item}' not found in the inventory.")
        return

    available_quantity = inventory_df.loc[inventory_df['Product'] == new_item, 'Quantity'].values[0]
    quantity = int(input("How many do you want? "))
    if quantity > available_quantity:
        print(f"Only {available_quantity} available in inventory.")
        return

    item_price = inventory_df.loc[inventory_df['Product'] == new_item, 'Price'].values[0]

    inventory_df.loc[inventory_df['Product'] == new_item, 'Quantity'] -= quantity

    if new_item in cart_df['Product'].str.capitalize().values:
        cart_df.loc[cart_df['Product'] == new_item, 'Quantity'] += quantity

        cart_df.loc[cart_df['Product'] == new_item, 'Total Cost'] = (
            round(cart_df.loc[cart_df['Product'] == new_item, 'Quantity'] * item_price, 2)
        )

        inventory_df.to_csv(inventory_file_path, index=False)
        cart_df.to_csv(customer_cart_file_path, index=False)

        print("Product added to the cart!")
        format_table(cart_df)
        return

    new_row = pd.DataFrame({
        'Product': [new_item],
        'Price': [item_price],
        'Quantity': [quantity],
        'Total Cost': [round((item_price * quantity), 2)]
    })

    new_row = new_row.dropna(axis=1, how='all')
    if not new_row.empty:
        cart_df = pd.concat([cart_df, new_row], ignore_index=True)

    inventory_df.to_csv(inventory_file_path, index=False)
    cart_df.to_csv(customer_cart_file_path, index=False)

    print("Product added to the cart!")
    format_table(cart_df)


def quantity_edit():
    inventory_df = pd.read_csv(inventory_file_path)
    cart_df = pd.read_csv(customer_cart_file_path)

    item_name = input("Enter your item: ").strip().capitalize()
    if item_name not in cart_df['Product'].str.capitalize().values:
        print(f"'{item_name}' not found in the inventory.")
        return


    choice = input("Do you wanna (increase) or (decrease) the quantity?").lower()
    if choice == "increase":
        available_quantity_in_store = inventory_df.loc[inventory_df['Product'] == item_name, 'Quantity'].values[0]
        quantity = int(input("How many do you want to add? "))
        if quantity > available_quantity_in_store:
            print(f"Only {available_quantity_in_store} available in inventory.")
            return

        item_price = inventory_df.loc[inventory_df['Product'] == item_name, 'Price'].values[0]
        inventory_df.loc[inventory_df['Product'] == item_name, 'Quantity'] -= quantity
        cart_df.loc[cart_df['Product'] == item_name, 'Quantity'] += quantity
        cart_df.loc[cart_df['Product'] == item_name, 'Total Cost'] = (
            round(cart_df.loc[cart_df['Product'] == item_name, 'Quantity'] * item_price, 2)
        )

        inventory_df.to_csv(inventory_file_path, index=False)
        cart_df.to_csv(customer_cart_file_path, index=False)

        print("Product updated!")
        format_table(cart_df)
        return

    elif choice == "decrease":
        available_quantity_in_cart = cart_df.loc[cart_df['Product'] == item_name, 'Quantity'].values[0]
        quantity = int(input("How many do you want to return back? "))
        if quantity > available_quantity_in_cart:
            print(f"Only {available_quantity_in_cart} available in cart.")
            return

        item_price = inventory_df.loc[inventory_df['Product'] == item_name, 'Price'].values[0]
        inventory_df.loc[inventory_df['Product'] == item_name, 'Quantity'] += quantity
        cart_df.loc[cart_df['Product'] == item_name, 'Quantity'] -= quantity
        cart_df.loc[cart_df['Product'] == item_name, 'Total Cost'] = (
            round(cart_df.loc[cart_df['Product'] == item_name, 'Quantity'] * item_price, 2)
        )

        inventory_df.to_csv(inventory_file_path, index=False)
        cart_df.to_csv(customer_cart_file_path, index=False)

        print("Product updated!")
        format_table(cart_df)
        return
    else:
        print("Wrong input!")
        show_edit_menu()
        return


def delete_product():
    inventory_df = pd.read_csv(inventory_file_path)
    cart_df = pd.read_csv(customer_cart_file_path)

    item_name = input("Enter the item that you want to remove: ").capitalize()

    if item_name not in cart_df['Product'].values:
        print(f"'{item_name}' not found in the cart.")
        return
    restored_quantity = cart_df.loc[cart_df['Product'] == item_name, 'Quantity'].values[0]
    inventory_df.loc[inventory_df['Product'] == item_name, 'Quantity'] += restored_quantity
    cart_df = cart_df[cart_df['Product'] != item_name]

    inventory_df.to_csv(inventory_file_path, index=False)
    cart_df.to_csv(customer_cart_file_path, index = False)

    print(f"'{item_name}' has been removed from your cart.")
    format_table(cart_df)

def sort_products():
    cart_df = pd.read_csv(customer_cart_file_path)
    cart_df.sort_values(by='Product', inplace=True)

    cart_df.to_csv(customer_cart_file_path, index=False)
    format_table(cart_df)


def create_receipt():
    receipt_df = pd.read_csv(customer_cart_file_path)
    total_cost = round(receipt_df['Total Cost'].sum(), 2)
    Quantity = receipt_df['Quantity'].sum()

    total_row = pd.DataFrame([['TOTAL', Quantity, '---', total_cost]], columns=receipt_df.columns)
    receipt_df = pd.concat([receipt_df, total_row], ignore_index=True)

    receipt_df.to_csv(final_receipt_file_path, index=False)
    format_table(receipt_df)

    print("Receipt successfully saved.")


def reset_inventory_and_cart():
        shutil.copy(original_inventory, inventory_file_path)
        print("Inventory has been reset to its original state.")

        shutil.copy(original_cart, customer_cart_file_path)
        print("Cart has been reset to its original state (empty except for headers).")

        shutil.copy(original_receipt, final_receipt_file_path)
        print("Receipt has been reset to its original state.")


def exit_program():
    print("Exiting the program...")
    reset_inventory_and_cart()
    print("\nGoodBye; We will be waiting for you! =)")
    exit()

