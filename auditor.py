# INF1103 - Week 2
# Smart Inventory Auditor

def main():
    # Requirement 1: Initialise inventory to zero
    inventory = 0
    failed_entries = 0

    print("==== Smart Inventory Auditor ====")
    print("Enter a stock quantity, or type 'quit' to stop.\n")

    # Requirement 2: Loop until user types 'quit'
    while True:
        entry = input("Enter stock quantity: ").strip

        if entry.lower() == "quit":
            break

main()