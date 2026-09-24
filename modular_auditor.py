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


def process_delivery(current_total, new_value):
    """
    Adds one delivery to the running inventory total.
    Takes: current_total (int), new_value (int)
    Returns: the updated total (int)
    """


def calculate_tax(amount):
    """
    Calculates 10% tax on a single delivery.
    Takes: amount (int)
    Returns: the tax owed on that delivery (float)
    """


def generate_report(total_units, failed_attempts):
    """
    Prints the closing summary. Pure I/O function - no return value needed.
    Takes: total_units (int), failed_attempts (int)
    Returns: nothing
    """





def main():
    # Requirement 1: Initialise inventory to zero
    inventory = 0
    failed_entries = 0

    print("==== Smart Inventory Auditor ====")
    print("Enter a stock quantity, or type 'quit' to stop.\n")

    # Requirement 2: Loop until user types "quit"
    while True:
        entry = input("Enter stock quantity: ").strip()

        if entry.lower() == "quit":
            break

        # Requirement 4: Reject invalid inputs
        if entry.isdigit():
            quantity = int(entry)
        elif entry.startswith("-") and entry[1:].isdigit():
            quantity = int(entry)
        else:
            print("Rejected: '{}' is not a valid input.".format(entry))
            failed_entries += 1
            continue

        # Requirement 3: Accepting stock values as integers
        quantity = int(entry)

        # Requirement 5: Reject negative stock values
        if quantity < 0:
            print("Rejected: '{}' is a negative number.".format(entry))
            failed_entries += 1
            continue

        # Requirement 6: Keep a running total of the inventory
        inventory += quantity
        print("Accepted. Current total: {}".format(inventory))

        # Requirement 7: Overstock alert for quantities exceeding 500
        if inventory > 500:
            print("\n*** OVERSTOCK ALERT: Inventory exceeds 500 units! ***")
            print("Stopping intake immediately.\n")
            break

    # Requirement 8: Reporting
    print("\n==== Report ====")
    print("Total Units Processed: {}".format(inventory))
    print("Number of Failed/Rejected Entries: {}".format(failed_entries))

if __name__ == "__main__":
    main()