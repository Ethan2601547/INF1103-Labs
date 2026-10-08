# INF1103 Lab 5 - Data Manipulation
 
import json   # built-in module for reading/writing JSON files
import os     # built-in module, used here to check if a file exists
 
# The file where our inventory is stored. Kept in one variable so that
# if the filename ever changes, we only edit it in one place.
INVENTORY_FILE = "inventory.json"

# =====================================================================
# 1 - Data representation (dictionaries inside a list)
# =====================================================================
 
def create_sample_inventory():
    """Return a list containing three sample products.
 
    Each product is a DICTIONARY (key -> value pairs), and the inventory
    is a LIST of those dictionaries. This satisfies the requirement:
    'dictionaries ... store at least three products in a list'.
    """
    return [
        {"id": "P001", "name": "Laptop",   "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse",    "price": 25.50,   "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00,   "stock": 25},
    ]

# =====================================================================
# 2 - Persistence: load_inventory()
# =====================================================================
 
def load_inventory():
    """Load the inventory list from inventory.json.
 
    - If the file exists: read it and return the list inside.
    - If it does not exist (or is unreadable): return an EMPTY list so
      the program keeps running without crashing.
    """
    # os.path.exists() returns True/False depending on whether the file is there
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            # 'with' automatically closes the file when the block ends
            with open(INVENTORY_FILE, "r") as file:
                inventory = json.load(file)   # JSON text -> Python list
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            # File exists but is corrupted/unreadable: don't crash, start fresh
            print("Could not read inventory file. Starting with empty inventory.")
            return []
    else:
        print(f"{INVENTORY_FILE} not found. Starting with empty inventory.")
        return []

# =====================================================================
# 3 - Persistence: save_inventory()
# =====================================================================
 
def save_inventory(inventory):
    """Write the inventory list to inventory.json."""
    with open(INVENTORY_FILE, "w") as file:   # "w" = write (overwrites old file)
        json.dump(inventory, file, indent=4)  # Python list -> JSON text; indent=4 = readable
    print(f"Inventory saved successfully to {INVENTORY_FILE}.")

# =====================================================================
# Data manipulation functions (add / update / search / display)
# =====================================================================

def search_product(inventory, product_id):
    """Return the product dictionary with this ID, or None if not found."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None   # loop finished without finding a match


def add_product(inventory, product_id, name, price, stock):
    """Add a new product. Return True if added, False if the ID already exists."""
    # Business rule: product IDs must be unique
    if search_product(inventory, product_id) is not None:
        return False
    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    }
    inventory.append(new_product)   # add the dictionary to the end of the list
    return True


def update_stock(inventory, product_id, new_stock):
    """Set a product's stock to new_stock. Return True if updated, False if not found."""
    product = search_product(inventory, product_id)
    if product is None:
        return False
    product["stock"] = new_stock    # dictionaries are mutable, so this edits the list in place
    return True


def display_all(inventory):
    """Print every product in a formatted list."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if len(inventory) == 0:
        print("No products in inventory.")
    else:
        for p in inventory:
            # :.2f formats the price with exactly 2 decimal places
            print(f"ID: {p['id']} | Name: {p['name']} | "
                  f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)

# =====================================================================
# Input helpers - keep validation separate so the menu code stays clean
# =====================================================================

def get_non_negative_int(prompt):
    """Keep asking until the user enters a whole number >= 0."""
    while True:
        text = input(prompt).strip()
        if text.isdigit():          # isdigit() is False for letters, decimals and negatives
            return int(text)
        print("Invalid input. Please enter a whole number (0 or more).")


def get_non_negative_float(prompt):
    """Keep asking until the user enters a number >= 0 (decimals allowed)."""
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)     # raises ValueError if text isn't a number
            if value >= 0:
                return value
            print("Price cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a number (e.g. 299.99).")

# =====================================================================
# Menu handlers - one function per menu option
# =====================================================================
 
def handle_add(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()   # P004, p004 -> P004
    name = input("Product Name: ").strip()
    if product_id == "" or name == "":
        print("Product ID and Name cannot be empty.")
        return
    price = get_non_negative_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")
 
    if add_product(inventory, product_id, name, price, stock):
        print("Product added successfully!")
    else:
        print(f"A product with ID {product_id} already exists.")


def handle_update(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    new_stock = get_non_negative_int("New Stock Quantity: ")
    update_stock(inventory, product_id, new_stock)
    print("Stock updated successfully!")


def handle_search(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# =====================================================================
# Main program loop - runs until the user chooses to exit
# =====================================================================
 
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
 
    inventory = load_inventory()   # read saved data into memory at startup
 
    # Loop until the user chooses Exit (option 6)
    while True:
        print_menu()
        choice = input("Enter option: ").strip()
 
        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            handle_add(inventory)
        elif choice == "3":
            handle_update(inventory)
        elif choice == "4":
            handle_search(inventory)
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)     # auto-save on exit, as in the sample output
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break                         # leaves the while loop -> program ends
        else:
            print("Invalid option. Please choose 1-6.")
 
 
# Only run main() when this file is executed directly (not when imported)
if __name__ == "__main__":
    main()