# INF1103 - Week 3
# Smart Inventory Auditor (Modular Version)


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
    # Requirement 1: Initialise inventory to zero
    inventory = 0
    failed_entries = 0

    print("==== Smart Inventory Auditor (Modular) ====")
    print("Enter a stock quantity, or type 'quit' to stop.\n")

    # Requirement 2: Loop until user types "quit"
    while True:
        result = get_valid_input()

        if result == "quit":
            break

        # Requirement 4: Reject invalid inputs
        if result is None:
            failed_entries += 1
            continue

        quantity = result
        inventory = process_delivery(inventory, quantity)
        tax = calculate_tax(quantity)

        print("Accepted. Delivery: {} | Tax owed: {:.2f} | Current total: {}".format(quantity, tax, inventory))

        # Requirement 7: Overstock alert for quantities exceeding 500
        if inventory > 500:
            print("\n*** OVERSTOCK ALERT: Inventory exceeds 500 units! ***")
            print("Stopping intake immediately.\n")
            break

    # Requirement 8: Reporting
    generate_report(inventory, failed_entries)

if __name__ == "__main__":
    main()