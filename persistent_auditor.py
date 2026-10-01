# INF1103 - Week 4
# Smart Inventory Auditor (Persistent Version)
import os

#Requirement 1: Persistence
def load_inventory():
    filename = "inventory.txt"
    if not os.path.exists(filename):
        return 0, []

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            if not lines:
                return 0, []

            total = int(lines[0].strip())
            history = []
            for line in lines[1:]:
                if line.strip():
                    history.append(int(line.strip()))

            return total, history
    except Exception:
        return 0, []

def save_inventory(total, history):
    with open("inventory.txt", "w") as file:
        file.write("Total Deliveries: {}\n".format(total))
        for item in history:
            file.write("Stock Quantity: {}\n".format(item))

def get_valid_input():
    """
    Prompts the user for a single stock quantity and validates it.
    Takes: nothing
    Returns: a non-negative integer on success,
    the string "quit" if the user wants to stop,
    or None if the entry was rejected.
    """
    entry = input("Enter stock quantity:").strip()

    if entry.lower() == "quit":
        return "quit"

    if entry.isdigit():
        return int(entry)
    elif entry.startswith("-") and entry[1:].isdigit():
        print("Rejected: '{}' is a negative number.".format(entry))
        return None
    else:
        print("Rejected: '{}' is not a valid input.".format(entry))
        return None
    

def process_delivery(current_total, new_value):
    """
    Adds one delivery to the running inventory total.
    Takes: current_total (int), new_value (int)
    Returns: the updated total (int)
    """
    return current_total + new_value


def calculate_tax(amount):
    """
    Calculates 10% tax on a single delivery.
    Takes: amount (int)
    Returns: the tax owed on that delivery (float)
    """
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """
    Prints the closing summary. Pure I/O function - no return value needed.
    Takes: total_units (int), failed_attempts (int)
    Returns: nothing
    """
    print("\n==== Report ====")
    print("Total Deliveries Processed: {}".format(total_units))
    print("Number of Failed/Rejected Entries: {}".format(failed_attempts))



def main():
    inventory, history = load_inventory()
    failed_entries = 0

    print("==== Smart Inventory Auditor (Modular) ====")
    print("Enter a stock quantity, or type 'quit' to stop.\n")

    while True:
        result = get_valid_input()

        if result == "quit":
            #Requirement 3: Write-back - Save when user quits
            save_inventory(inventory, history)
            print("Data successfully saved to inventory.txt.")
            break

        if result is None:
            failed_entries += 1
            continue

        quantity = result
        inventory = process_delivery(inventory, quantity)
        tax = calculate_tax(quantity)

        #Requirement 2: History Tracking using Python list (array)
        history.append(quantity)

        print("Accepted. Delivery: {} | Tax owed: {:.2f} | Current total: {}".format(quantity, tax, inventory))

        if inventory > 500:
            print("\n*** OVERSTOCK ALERT: Inventory exceeds 500 units! ***")
            print("Stopping intake immediately.\n")
            save_inventory(inventory, history)
            print("Data successfully saved to inventory.txt.")
            break

    generate_report(inventory, failed_entries)

if __name__ == "__main__":
    main()