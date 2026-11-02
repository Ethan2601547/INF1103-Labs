#file_handler.py
#responsible for saving and loading the inventory as JSON

import json
import os

from product import Product
from inventory import Inventory

INVENTORY_FILE = "inventory.json"

def inventory_file_exists(filename=INVENTORY_FILE):
    return os.path.exists(filename)

def save_inventory(inventory, filename=INVENTORY_FILE):
    records = []
    for product in inventory.get_products():
        records.append({
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        })

    with open(filename, "w") as file:
        json.dump(records, file, indent=4)
    print(f"Inventory saved successfully to {filename}.")

def load_inventory(filename=INVENTORY_FILE):
    inventory = Inventory()
    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with empty inventory.")
        return inventory

    print(f"{filename} found.")
    try:
        with open(filename, "r") as file:
            records = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read inventory file. Starting with empty inventory.")
        return inventory

    for record in records:
        try:
            product = Product(record["id"], record["name"], record["price"], record["stock"])
            inventory.add_product(product)
        except (KeyError, ValueError, TypeError):
            print(f"Skipped an invalid record: {record}.")

    print(f"Inventory loaded successfully.")
    return inventory