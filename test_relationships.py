#test_relationships.py
#Lab 8 test code: association, aggregation, composition, LSP and polymorphism.
#Run with:  python test_relationships.py
#Every "PASS/FAIL" line is a check. The other lines show what the objects print.
#It writes a temporary JSON file and deletes it at the end.

import os

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from order_line import OrderLine
from file_handler import save_data, load_data


def check(description: str, condition: bool) -> None:
    print(("PASS" if condition else "FAIL") + " - " + description)


def test_association() -> None:
    print("\n===== ASSOCIATION: Supplier and Product (Section 2) =====")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
    ebook = DigitalProduct("P002", "Python E-Book", 12.00, 200, supplier, 8.5)

    print("Supplier information shown through each Product:")
    laptop.supplier.display_information()
    ebook.supplier.display_information()

    check("Product stores a reference to its Supplier", laptop.supplier is supplier)
    check("Both products refer to the SAME Supplier object", laptop.supplier is ebook.supplier)

    #PREDICT FIRST: what happens to the products after 'del supplier'?
    del supplier
    print("After 'del supplier', asking the products for their supplier again:")
    laptop.supplier.display_information()
    ebook.supplier.display_information()
    check("Product can still show its supplier after 'del supplier'", laptop.supplier.name == "TechSource Pte Ltd")

    lonely_supplier = Supplier("S099", "No Products Ltd", "hello@noproducts.example")
    check("A Supplier can exist with no products at all", lonely_supplier.name == "No Products Ltd")


def test_aggregation() -> None:
    print("\n===== AGGREGATION: Inventory and Product (Section 3) =====")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    mouse = PhysicalProduct("P003", "Mouse", 25.50, 40, supplier, 1.0)     #created BEFORE any inventory
    inventory_a = Inventory()
    inventory_b = Inventory()

    check("Product exists before being added to any Inventory", mouse.name == "Mouse")
    check("Product is added to Inventory A", inventory_a.add_product(mouse))
    check("Inventory A finds the very same object", inventory_a.find_product("P003") is mouse)
    check("A duplicate ID is rejected", not inventory_a.add_product(mouse))

    #PREDICT FIRST: will the Product still work after it is removed from Inventory A?
    removed = inventory_a.remove_product("P003")
    check("remove_product returns the removed Product", removed is mouse)
    check("Inventory A no longer contains it", inventory_a.find_product("P003") is None)
    print("The removed product can still be used:")
    mouse.display_information()
    mouse.update_stock(35)
    check("Product still works after removal (stock updated to 35)", mouse.stock == 35)

    check("The same Product object is added to Inventory B", inventory_b.add_product(mouse))
    check("Inventory B holds the same object", inventory_b.find_product("P003") is mouse)

    inventory_b.remove_product("P003")
    check("Emptying an inventory leaves it with no products", len(inventory_b.get_products()) == 0)
    check("...but the Product itself still exists", mouse.name == "Mouse" and mouse.stock == 35)
    check("Removing a missing ID returns None", inventory_a.remove_product("P999") is None)


def test_composition() -> None:
    print("\n===== COMPOSITION: Order and OrderLine (Section 4) =====")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
    mouse = PhysicalProduct("P003", "Mouse", 25.50, 40, supplier, 1.0)

    order1 = Order("O001")
    order1.add_order_line(laptop, 1)                    #the Order creates the OrderLine itself
    order1.add_order_line(mouse, 2)
    order1.display_information()
    check("Order total uses its order lines (1200.00 + 2 x 25.50 = 1251.00)",
          abs(order1.calculate_total() - 1251.00) < 0.001)

    #PREDICT FIRST: same Product in two different Orders. How many OrderLines? How many Products?
    order2 = Order("O002")
    order2.add_order_line(laptop, 3)
    line_in_order1: OrderLine = order1.get_order_lines()[0]
    line_in_order2: OrderLine = order2.get_order_lines()[0]
    print(f"OrderLine in order 1: id {id(line_in_order1)}   OrderLine in order 2: id {id(line_in_order2)}")
    print(f"Product in order 1:   id {id(line_in_order1.product)}   Product in order 2:   id {id(line_in_order2.product)}")
    check("Each Order created its OWN OrderLine object", line_in_order1 is not line_in_order2)
    check("Both lines refer to the SAME Product object", line_in_order1.product is line_in_order2.product)

    check("The Order removes one of its own lines", order1.remove_order_line("P003"))
    check("The order total updates after removing the line", abs(order1.calculate_total() - 1200.00) < 0.001)
    check("Removing an order line does NOT destroy the Product", mouse.name == "Mouse" and mouse.stock == 40)
    check("Order 2 is unaffected by changes to Order 1", abs(order2.calculate_total() - 3600.00) < 0.001)

    try:
        order1.add_order_line(laptop, 0)
        check("A quantity of 0 is rejected", False)
    except ValueError:
        check("A quantity of 0 is rejected", True)


def show_product_details(product: Product) -> None:
    #Works with ANY Product. It never asks which subclass it is. (Section 6.2)
    product.display_information()
    print(product.get_fulfillment_info())


def test_lsp_and_polymorphism() -> None:
    print("\n===== LSP AND POLYMORPHISM (Sections 6 and 7) =====")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    physical = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
    digital = DigitalProduct("P004", "Antivirus Software", 49.90, 100, supplier, 250.5)

    print("show_product_details() called with a PhysicalProduct, then a DigitalProduct:")
    show_product_details(physical)
    show_product_details(digital)

    inventory = Inventory()
    check("PhysicalProduct can be added through the Product abstraction", inventory.add_product(physical))
    check("DigitalProduct can be added through the Product abstraction", inventory.add_product(digital))

    #PREDICT FIRST: what will get_fulfillment_info() print for each product?
    print("One loop over the Product collection, no isinstance():")
    messages: list[str] = []
    for product in inventory.get_products():
        product.display_information()
        message = product.get_fulfillment_info()
        print(message)
        messages.append(message)
    check("Physical and digital products give different, specialised messages", messages[0] != messages[1])
    check("Physical message mentions shipping", "shipping" in messages[0].lower())
    check("Digital message mentions download", "download" in messages[1].lower())

    print("LSP: the parent's expectation about update_stock() holds for both subclasses:")
    for product in inventory.get_products():
        product.update_stock(10)
        check(f"{product.name}: update_stock(10) sets the stock to 10", product.stock == 10)
        try:
            product.update_stock(-1)
            check(f"{product.name}: update_stock(-1) is rejected", False)
        except ValueError:
            check(f"{product.name}: update_stock(-1) is rejected", True)
    check("DigitalProduct inherits update_stock unchanged (does not override it)",
          DigitalProduct.update_stock is Product.update_stock)
    check("PhysicalProduct inherits update_stock unchanged (does not override it)",
          PhysicalProduct.update_stock is Product.update_stock)

    try:
        Product("X1", "Generic", 1.0, 1, supplier)       # type: ignore[abstract]
        check("Product itself cannot be created (abstract)", False)
    except TypeError:
        check("Product itself cannot be created (abstract)", True)
    check("PhysicalProduct is a CanBeShipped, DigitalProduct is not",
          isinstance(physical, CanBeShipped) and not isinstance(digital, CanBeShipped))


def test_persistence() -> None:
    print("\n===== PERSISTENCE KEEPS THE RELATIONSHIPS (Section 9) =====")
    supplier1 = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    supplier2 = Supplier("S002", "SoftServe Digital", "orders@softserve.example")
    unused_supplier = Supplier("S003", "No Products Ltd", "hello@noproducts.example")
    suppliers = {s.supplier_id: s for s in (supplier1, supplier2, unused_supplier)}

    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier1, 2.5))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, supplier1, 1.0))
    inventory.add_product(DigitalProduct("P004", "Antivirus", 49.90, 100, supplier2, 250.5))

    test_file = "test_inventory.json"
    save_data(inventory, suppliers, test_file)
    loaded_inventory, loaded_suppliers = load_data(test_file)
    os.remove(test_file)

    laptop = loaded_inventory.find_product("P001")
    mouse = loaded_inventory.find_product("P002")
    antivirus = loaded_inventory.find_product("P004")
    check("All 3 suppliers are restored (even the one with no products)", len(loaded_suppliers) == 3)
    check("All 3 products are restored", len(loaded_inventory.get_products()) == 3)
    check("Loaded product refers to the right supplier",
          laptop is not None and laptop.supplier.supplier_id == "S001")
    check("Two products of one supplier share ONE Supplier object after loading",
          laptop is not None and mouse is not None and laptop.supplier is mouse.supplier)
    check("The digital product refers to its own supplier",
          antivirus is not None and antivirus.supplier is loaded_suppliers["S002"])


test_association()
test_aggregation()
test_composition()
test_lsp_and_polymorphism()
test_persistence()