#main.py
#Shows the menu, get user input, and calls the Iventory methods. Never changes product data directly.

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from file_handler import save_inventory, load_inventory, inventory_file_exists

def get_non_negative_int(prompt):
    while True:
        text = input(prompt).strip()
        if text.isdigit():
            return int(text)
        print("Invalid input. Please enter a whole number (0 or more).")

def get_non_negative_float(prompt):
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
            if value >= 0:
                return value
            print("Value cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a valid number (eg. 299.99).")


def get_product_type():
    while True:
        print("Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        choice = input("Choose product type (1-2): ").strip()
        if choice == "1":
            return "physical"
        if choice == "2":
            return "digital"
        print("Invalid choice. Please enter 1 or 2.")
        

def create_sample_inventory():
    inventory = Inventory()

    product1 = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5)
    product2 = PhysicalProduct("P002", "Mouse", 25.50, 40, 1.0)
    product3 = PhysicalProduct("P003", "Keyboard", 45.00, 25, 2.0)

    product4 = DigitalProduct("P004", "Antivirus Software", 49.90, 100, 250.5)
    product5 = DigitalProduct("P005", "Python E-Book", 12.00, 200, 8.5)

    inventory.add_product(product1)
    inventory.add_product(product2)
    inventory.add_product(product3)
    inventory.add_product(product4)
    inventory.add_product(product5)
    return inventory

def handle_add(inventory):
    print("\nAdd a New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Product ID cannot be empty.")
        return

    if inventory.search_product(product_id) is not None:
        print(f"Product ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    if name == "":
        print("Product Name cannot be empty.")
        return

    product_type = get_product_type()
    price = get_non_negative_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    if product_type == "physical":
        weight = get_non_negative_float("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = get_non_negative_float("Download Size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size)

    if inventory.add_product(product):
        print(f"Product {product_id} added successfully.")
    else:
        print(f"Product ID {product_id} already exists.")

def handle_update(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID to update: ").strip().upper()
    product = inventory.search_product(product_id)
    if product is None:
        print(f"Product ID {product_id} not found.")
        return
    print("Product found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    new_stock = get_non_negative_int("Enter New Stock Quantity: ")
    try:
        inventory.update_stock(product_id, new_stock)
        print(f"Stock for Product ID {product_id} updated successfully.")
    except ValueError as error:
        print(f"Could not update stock: {error}")

def handle_search(inventory):
    print("\nSearch for a Product")
    product_id = input("Enter Product ID to search: ").strip().upper()
    product = inventory.search_product(product_id)
    if product is None:
        print(f"Product ID {product_id} not found.")
        return
    print("Product found:")
    print("-" * 48)
    product.display_information()
    print(f"    Fulfillment: {product.get_fulfillment_info()}")
    print("-" * 48)

def print_menu():
    print("\n-------- Menu --------")
    print("1. Display All Products")
    print("2. Add a New Product")
    print("3. Update Stock")
    print("4. Search for a Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------")

def main():
    print("=" * 40)
    print("Inventory Management System (OOP)")
    print("=" * 40)

    if inventory_file_exists():
        inventory = load_inventory()
    else:
        print("No saved inventory found. Creating a sample inventory.")
        inventory = create_sample_inventory()

    while True:
        print_menu()
        choice = input("Enter option (1-6): ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            handle_add(inventory)
        elif choice == "3":
            handle_update(inventory)
        elif choice == "4":
            handle_search(inventory)
        elif choice == "5":
            print("Inventory saving...")
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exiting...")
            save_inventory(inventory)
            print("System exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1-6.")

if __name__ == "__main__":
    main()