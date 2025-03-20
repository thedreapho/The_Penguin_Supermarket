import pandas as pd
import shutil

# File paths for various databases
inventory_file_path = "D:\Coding\my codings\AllOfTheCodes\Final_Project\database\penguin_sm_inventory.csv"
customer_cart_file_path = "D:\Coding\my codings\AllOfTheCodes\Final_Project\database\customer_cart.csv"
final_receipt_file_path = r"D:\Coding\my codings\AllOfTheCodes\Final_Project\database\final_receipt.csv"

original_inventory = "D:\Coding\my codings\AllOfTheCodes\Final_Project\database\original_inventory.csv"
original_cart = "D:\Coding\my codings\AllOfTheCodes\Final_Project\database\original_cart.csv"
original_receipt = "D:\Coding\my codings\AllOfTheCodes\Final_Project\database\original_receipt.csv"


# --------------------------------------------------------

def format_table(df):
    """
    Formats and prints a table representation of the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to format and display.

    Returns:
        None
    """
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
    """
    Displays the main menu options to the user and handles user input.

    Options include:
        - View inventory
        - View your cart
        - Edit your cart
        - Create a receipt
        - Exit the program

    Returns:
        None
    """
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
            elif action == 'Edit your cart':
                show_edit_menu()
            elif action == 'Create receipt':
                create_receipt()
            elif action == 'Exit':
                exit_program()
            else:
                print("Invalid choice. Please try again.")


def view_inventory():
    """
    Displays the current inventory of products.

    Returns:
        None
    """
    inventory_df = pd.read_csv(inventory_file_path)
    format_table(inventory_df)


def view_your_cart():
    """
    Displays the current items in the user's shopping cart.

    Returns:
        None
    """
    cart_df = pd.read_csv(customer_cart_file_path)
    format_table(cart_df)


def show_edit_menu():
    """
    Displays the edit menu where users can modify their cart.

    Options include:
        - Add a product to your cart
        - Edit the quantity of an item
        - Sort products in your cart
        - Delete an item from your cart
        - Back to Main Menu

    Returns:
        None
    """
    edit_menu_data = {
        'Option': [1, 2, 3, 4, 5],
        'Action': [
            'Add a product to your cart',
            'Edit the quantity of an item',
            'Sort products in your cart',
            'Delete an item from your cart permanently',
            'Back to Main Menu'
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
            elif action == 'Edit the quantity of an item':
                quantity_edit()
            elif action == 'Sort products in your cart':
                sort_products()
            elif action == 'Delete an item from your cart permanently':
                delete_product()
            elif action == 'Back to Main Menu':
                show_main_menu()
            else:
                print("Invalid choice. Please try again.")


def add_product():
    """
    Adds a new product to the user's cart. Checks inventory for availability and updates the cart accordingly.

    Returns:
        None
    """
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

    # Update inventory and cart
    inventory_df.loc[inventory_df['Product'] == new_item, 'Quantity'] -= quantity

    if new_item in cart_df['Product'].str.capitalize().values:
        cart_df.loc[cart_df['Product'] == new_item, 'Quantity'] += quantity
        cart_df.loc[cart_df['Product'] == new_item, 'Total Cost'] = (
            round(cart_df.loc[cart_df['Product'] == new_item, 'Quantity'] * item_price, 2)
        )
        print("Product added to the cart!")
    else:
        new_row = pd.DataFrame({
            'Product': [new_item],
            'Price': [item_price],
            'Quantity': [quantity],
            'Total Cost': [round((item_price * quantity), 2)]
        })
        new_row = new_row.dropna(axis=1, how='all')
        if not new_row.empty:
            cart_df = pd.concat([cart_df, new_row], ignore_index=True)
        print("Product added to the cart!")

    inventory_df.to_csv(inventory_file_path, index=False)
    cart_df.to_csv(customer_cart_file_path, index=False)
    format_table(cart_df)


def quantity_edit():
    """
    Edits the quantity of an item in the user's cart, either increasing or decreasing it.

    Returns:
        None
    """
    inventory_df = pd.read_csv(inventory_file_path)
    cart_df = pd.read_csv(customer_cart_file_path)

    item_name = input("Enter your item: ").strip().capitalize()
    if item_name not in cart_df['Product'].str.capitalize().values:
        print(f"'{item_name}' not found in the cart.")
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
        print("Product updated!")
    elif choice == "decrease":
        available_quantity_in_cart = cart_df.loc[cart_df['Product'] == item_name, 'Quantity'].values[0]
        quantity = int(input(f"How many do you want to remove (max {available_quantity_in_cart})? "))
        if quantity > available_quantity_in_cart:
            print(f"You can't remove more than {available_quantity_in_cart}.")
            return

        item_price = inventory_df.loc[inventory_df['Product'] == item_name, 'Price'].values[0]
        inventory_df.loc[inventory_df['Product'] == item_name, 'Quantity'] += quantity
        cart_df.loc[cart_df['Product'] == item_name, 'Quantity'] -= quantity
        cart_df.loc[cart_df['Product'] == item_name, 'Total Cost'] = (
            round(cart_df.loc[cart_df['Product'] == item_name, 'Quantity'] * item_price, 2)
        )
        print("Product updated!")

    inventory_df.to_csv(inventory_file_path, index=False)
    cart_df.to_csv(customer_cart_file_path, index=False)
    format_table(cart_df)


def delete_product():
    """
    Permanently removes an item from the user's cart.

    Returns:
        None
    """
    cart_df = pd.read_csv(customer_cart_file_path)
    item_name = input("Enter your item: ").strip().capitalize()
    if item_name not in cart_df['Product'].str.capitalize().values:
        print(f"'{item_name}' not found in the cart.")
        return

    cart_df = cart_df[cart_df['Product'] != item_name]
    cart_df.to_csv(customer_cart_file_path, index=False)
    print(f"'{item_name}' removed from the cart.")

def sort_products():
    """
    Sorts the products in the cart alphabetically by their product name.

    This function reads the cart data from the `customer_cart_file_path`, sorts
    the products based on the 'Product' column in alphabetical order, then
    saves the sorted data back to the same file. It also displays the updated
    cart to the user.

    Returns:
        None
    """
    # Read the cart data from the CSV file
    cart_df = pd.read_csv(customer_cart_file_path)

    # Sort the cart items alphabetically by product name
    cart_df.sort_values(by='Product', inplace=True)

    # Save the sorted cart back to the CSV file
    cart_df.to_csv(customer_cart_file_path, index=False)

    # Display the updated cart with sorted products
    format_table(cart_df)

def create_receipt():
    """
    Generates and displays the receipt based on the user's cart, then saves it as a CSV.

    Returns:
        None
    """
    cart_df = pd.read_csv(customer_cart_file_path)
    if cart_df.empty:
        print("Your cart is empty.")
        return

    total_cost = cart_df['Total Cost'].sum()
    cart_df.loc[cart_df.index[-1] + 1] = ['TOTAL', '', '', total_cost]

    cart_df.to_csv(final_receipt_file_path, index=False)
    print("Receipt created!")
    format_table(cart_df)


def reset_inventory_and_cart():
    """
    Resets the inventory, cart, and receipt files to their original state by
    copying backup files into their respective paths.

    This function ensures that the inventory and cart are reset to their
    initial condition (as specified in the backup files), and any changes
    made during the session are lost. This is useful when the user wants
    to restore the default state of the system.

    Returns:
        None
    """
    # Copy the original inventory file back to the current inventory path
    shutil.copy(original_inventory, inventory_file_path)
    print("Inventory has been reset to its original state.")

    # Copy the original cart file back to the current cart path
    shutil.copy(original_cart, customer_cart_file_path)
    print("Cart has been reset to its original state (empty except for headers).")

    # Copy the original receipt file back to the current receipt path
    shutil.copy(original_receipt, final_receipt_file_path)
    print("Receipt has been reset to its original state.")


def exit_program():
    """
    Exits the program after resetting the inventory, cart, and receipt files.

    This function first calls the reset_inventory_and_cart function to restore
    the inventory, cart, and receipt to their original states. It then prints
    a farewell message and exits the program.

    Returns:
        None
    """
    print("Exiting the program...")

    # Reset the inventory, cart, and receipt before exiting
    reset_inventory_and_cart()

    # Print a goodbye message
    print("\nGoodbye; We will be waiting for you! =)")

    # Exit the program
    exit()

