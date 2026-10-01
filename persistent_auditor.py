# INF1103 - Week 4
# Smart Inventory Auditor (Persistent Version)
import os

#Requirement 1: Persistence
def load_inventory():                           #Requirement 4: Create function load_inventory()
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

def save_inventory(total, history):             #Requirement 4: Create function save_inventory()
    with open("inventory.txt", "w") as file:
        file.write("{}\n".format(total))
        for item in history:
            file.write("{}\n".format(item))

def get_valid_input():
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
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts, history):
    print("\n==== Report ====")
    print("Total Deliveries Processed: {}".format(total_units))
    print("Number of Failed/Rejected Entries: {}".format(failed_attempts))
    print("Transaction History: {}".format(history))



def main():
    inventory, history = load_inventory()
    failed_entries = 0

    print("==== Smart Inventory Auditor (Persistent) ====")
    print("Loaded Previous Inventory Total: {}".format(inventory))

    #Prevent starting intake if already over the limit of 500
    if inventory > 500:
        print("\n*** OVERSTOCK ALERT: Inventory already exceeds 500 units! ***")
        print("Stopping intake immediately.\n")
        generate_report(inventory, failed_entries, history)
        return

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

        #Stop if current session total hits overstock limit of 500
        if inventory > 500:
            print("\n*** OVERSTOCK ALERT: Inventory exceeds 500 units! ***")
            print("Stopping intake immediately.\n")
            save_inventory(inventory, history)
            print("Data successfully saved to inventory.txt.")
            break
    
    generate_report(inventory, failed_entries, history)

if __name__ == "__main__":
    main()