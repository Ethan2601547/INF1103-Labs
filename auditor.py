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




if __name__ == "__main__":
    main()