#file_handler.py
#responsible for saving and loading the inventory as JSON

import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

INVENTORY_FILE = "inventory.json"

def inventory_file_exists(filename=INVENTORY_FILE):
    return os.path.exists(filename)

def save_inventory(inventory, filename=INVENTORY_FILE):
    records = []
    for product in inventory.get_products():
        record = {}

        if isinstance(product, PhysicalProduct):
            record["type"] = "physical"
        elif isinstance(product, DigitalProduct):
            record["type"] = "digital"
        else:
            print(f"Skipped product with unknown type: {product.product_id}.")
            continue

        record["id"] = product.product_id
        record["name"] = product.name
        record["price"] = product.price
        record["stock"] = product.stock

        if record["type"] == "physical":
            record["weight"] = product.weight
        else:
            record["download_size"] = product.download_size

        records.append(record)

    with open(filename, "w") as file:
        json.dump(records, file, indent=4)
    print(f"Inventory saved successfully to {filename}.")


def create_product_from_record(record):
    product_type = record["type"]
    if product_type == "physical":
        return PhysicalProduct(record["id"], record["name"], record["price"], record["stock"], record["weight"])
    elif product_type == "digital":
        return DigitalProduct(record["id"], record["name"], record["price"], record["stock"], record["download_size"])

    else:
        raise ValueError(f"Unknown product type: {product_type}.")


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
            product = create_product_from_record(record)
            inventory.add_product(product)
        except (KeyError, ValueError, TypeError):
            print(f"Skipped an invalid record: {record}.")

    print(f"Inventory loaded successfully.")
    return inventory