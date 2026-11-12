#main.py
#Shows the menu, gets user input, and calls the Inventory methods. Never changes product data directly.

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product import Product
from supplier import Supplier
from inventory import Inventory
from file_handler import save_data, load_data, inventory_file_exists

def get_non_negative_int(prompt: str) -> int:
    while True:
        text = input(prompt).strip()
        if text.isdigit():
            return int(text)
        print("Invalid input. Please enter a whole number (0 or more).")

def get_non_negative_float(prompt: str) -> float:
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
            if value >= 0:
                return value
            print("Value cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a valid number (eg. 299.99).")


def get_product_type() -> str:
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


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    #shows the existing suppliers and returns the one the user picks (or None)
    print("Available Suppliers:")
    for existing in suppliers.values():
        existing.display_information()
    supplier_id = input("Supplier ID: ").strip().upper()
    supplier = suppliers.get(supplier_id)
    if supplier is None:
        print(f"Supplier ID {supplier_id} not found.")
    return supplier


def create_sample_data() -> tuple[Inventory, dict[str, Supplier]]:
    #Suppliers are created FIRST and independently of any product (association)
    supplier1 = Supplier("S001", "Tech Pte Ltd", "sales@tech.example")
    supplier2 = Supplier("S002", "Popcorn Digital", "orders@popcorn.example")
    suppliers: dict[str, Supplier] = {
        supplier1.supplier_id: supplier1,
        supplier2.supplier_id: supplier2,
    }

    #Products are then created with a reference to their Supplier
    product1 = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier1, 2.5)
    product2 = PhysicalProduct("P002", "Mouse", 25.50, 40, supplier1, 1.0)
    product3 = PhysicalProduct("P003", "Keyboard", 45.00, 25, supplier1, 2.0)

    product4 = DigitalProduct("P004", "Antivirus Software", 49.90, 100, supplier2, 250.5)
    product5 = DigitalProduct("P005", "Python E-Book", 12.00, 200, supplier2, 8.5)

    #Inventory only gathers products that already exist (aggregation)
    inventory = Inventory()
    inventory.add_product(product1)
    inventory.add_product(product2)
    inventory.add_product(product3)
    inventory.add_product(product4)
    inventory.add_product(product5)
    return inventory, suppliers

def handle_add_supplier(suppliers: dict[str, Supplier]) -> None:
    print("\nAdd a New Supplier")
    supplier_id = input("Supplier ID: ").strip().upper()
    if supplier_id == "":
        print("Supplier ID cannot be empty.")
        return
    if supplier_id in suppliers:
        print(f"Supplier ID {supplier_id} already exists.")
        return

    name = input("Supplier Name: ").strip()
    contact_email = input("Contact Email: ").strip()
    try:
        suppliers[supplier_id] = Supplier(supplier_id, name, contact_email)
        print(f"Supplier {supplier_id} added successfully.")
    except ValueError as error:
        print(f"Could not add supplier: {error}")

def handle_add(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd a New Product")
    if len(suppliers) == 0:
        print("No suppliers available. Please add a supplier first (option 6).")
        return

    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Product ID cannot be empty.")
        return

    if inventory.find_product(product_id) is not None:
        print(f"Product ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    if name == "":
        print("Product Name cannot be empty.")
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    product_type = get_product_type()
    price = get_non_negative_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    product: Product                                        #either subclass fits, because both ARE Products
    try:
        if product_type == "physical":
            weight = get_non_negative_float("Weight (kg): ")
            product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        else:
            download_size = get_non_negative_float("Download Size (MB): ")
            product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
    except ValueError as error:
        print(f"Could not add product: {error}")
        return

    if inventory.add_product(product):
        print(f"Product {product_id} added successfully.")
    else:
        print(f"Product ID {product_id} already exists.")

def handle_update(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID to update: ").strip().upper()
    product = inventory.find_product(product_id)
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

def handle_search(inventory: Inventory) -> None:
    print("\nSearch for a Product")
    product_id = input("Enter Product ID to search: ").strip().upper()
    product = inventory.find_product(product_id)
    if product is None:
        print(f"Product ID {product_id} not found.")
        return
    print("Product found:")
    print("-" * 48)
    product.display_information()
    print(f"    Fulfillment: {product.get_fulfillment_info()}")
    print("    Supplier:")
    product.supplier.display_information()                  #the Product hands us its Supplier object
    print("-" * 48)

def print_menu() -> None:
    print("\n-------- Menu --------")
    print("1. Display All Products")
    print("2. Add a New Product")
    print("3. Update Stock")
    print("4. Search for a Product")
    print("5. Save Inventory")
    print("6. Add a New Supplier")
    print("7. Exit")
    print("----------------------")

def main() -> None:
    print("=" * 40)
    print("Inventory Management System (OOP)")
    print("=" * 40)

    if inventory_file_exists():
        inventory, suppliers = load_data()
    else:
        print("No saved inventory found. Creating a sample inventory.")
        inventory, suppliers = create_sample_data()

    while True:
        print_menu()
        choice = input("Enter option (1-7): ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            handle_add(inventory, suppliers)
        elif choice == "3":
            handle_update(inventory)
        elif choice == "4":
            handle_search(inventory)
        elif choice == "5":
            print("Inventory saving...")
            save_data(inventory, suppliers)
        elif choice == "6":
            handle_add_supplier(suppliers)
        elif choice == "7":
            print("Saving inventory before exiting...")
            save_data(inventory, suppliers)
            print("System exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1-7.")

if __name__ == "__main__":
    main()