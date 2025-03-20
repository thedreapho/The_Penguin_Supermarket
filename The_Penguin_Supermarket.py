import csv

def product_menu():
    print("Select the product that you want to add to your shopping cart: \n")

    with open("../database/penguin_sm_inventory.txt", mode="r", newline="") as inventory:
        reader = csv.reader(inventory)
        next(reader)
        print("-" * 44)
        print(f"| {'Product':<20} {'Quantity':<10} {'Price':<10}|")
        print("|" + "-" * 43 + "|")

        for row in reader:
            print(f"| {row[0].capitalize():<20} {row[1]:<10} {row[2]:<10}|")
        print("-" * 44)

print("Hiii :)\nWelcome to the Penguin sypermarket!\n")
