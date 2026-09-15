# INF1103 - Week 2
# Smart Inventory Auditor

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
        if not entry.isdigit():
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
            print("\n*** Overstock Alert!: Inventory exceeds 500 units! ***")
            print("Stopping input to prevent overstocking.\n")
            break

    # Requirement 8: Reporting
    print("\n==== Report ====")
    print("Total Units Processed: {}".format(inventory))
    print("Number of Failed/Rejected Entries: {}".format(failed_entries))

if __name__ == "__main__":
    main()