#file_handler.py
#responsible for saving and loading the inventory as JSON
#hold 2 lists now: suppliers and products
#each product refers to its supplier by supplier_id, which is how the association is maintained when saving and loading

import json
import os
from typing import Any

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product import Product
from supplier import Supplier
from inventory import Inventory
from product_factory import ProductFactory

INVENTORY_FILE = "inventory.json"

def inventory_file_exists(filename: str = INVENTORY_FILE) -> bool:
    return os.path.exists(filename)

def save_data(inventory: Inventory, suppliers: dict[str, Supplier], filename: str = INVENTORY_FILE) -> None:
    supplier_records: list[dict[str, str]] = []
    for supplier in suppliers.values():
        supplier_records.append({
            "supplier_id": supplier.supplier_id,
            "name": supplier.name,
            "contact_email": supplier.contact_email,
        })

    product_records: list[dict[str, str | int | float]] = []    
    for product in inventory.get_products():
        record: dict[str, str | int | float] = {}

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
        record["supplier_id"] = product.supplier.supplier_id

        if isinstance(product, PhysicalProduct):
            record["weight"] = product.weight
        elif isinstance(product, DigitalProduct):
            record["download_size"] = product.download_size

        product_records.append(record)

    data = {"suppliers": supplier_records, "products": product_records}
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory saved successfully to {filename}.")


def create_product_from_record(record: dict[str, Any], suppliers: dict[str, Supplier]) -> Product:
        supplier = suppliers[record["supplier_id"]]
        #a physical record stores "weight", a digital record stores "download_size"; the factory takes either as "size"
        size = record.get("weight", record.get("download_size", 0.0))
        return ProductFactory.create(record["type"], record["id"], record["name"], record["price"],
                                     record["stock"], supplier, size)


def load_data(filename: str = INVENTORY_FILE) -> tuple[Inventory, dict[str, Supplier]]:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with empty inventory.")
        return inventory, suppliers

    print(f"{filename} found.")
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read inventory file. Starting with empty inventory.")
        return inventory, suppliers

    if not isinstance(data, dict):
        print("This file is in the old format (no suppliers). Delete the file or replace it.")
        return inventory, suppliers

    for record in data.get("suppliers", []):
        try:
            supplier = Supplier(record["supplier_id"], record["name"], record["contact_email"])
            suppliers[supplier.supplier_id] = supplier
        except (KeyError, ValueError, TypeError):
            print(f"Skipped an invalid supplier record: {record}.")

    for record in data.get("products", []):
        try:
            product = create_product_from_record(record, suppliers)
            inventory.add_product(product)
        except (KeyError, ValueError, TypeError):
            print(f"Skipped an invalid record: {record}.")

    print(f"Inventory loaded successfully.")
    return inventory, suppliers