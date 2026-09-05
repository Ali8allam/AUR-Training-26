from pathlib import Path


def load_stock(filename):
    stock = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                if line.strip():
                    item, count = line.strip().split(",")
                    stock[item.lower()] = int(count)
    except FileNotFoundError:
        print("No stock file found. Starting with empty inventory.")
    return stock


def save_stock(filename, stock):
    with open(filename, "w") as file:
        for item, count in stock.items():
            file.write(f"{item},{count}\n")
    print("Stock saved successfully. Exiting program.")


def display_stock(stock):
    if not stock:
        print("Stock is empty.")
        return
    print("\n--- Current Inventory ---")
    for item, count in stock.items():
        print(f"{item.title()}: {count}")


def main():
    filename = Path(r"C:\Users\ALI & ADHM\Desktop\AUR-Training-26\task_2\subtask_1\stock.txt")
    stock = load_stock(filename)

    while True:
        print("\n1. Add Stock\n2. Remove Stock \n3. View Stock \n4. Save & Exit")
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            item = input("Enter item name: ").strip().lower()
            qty = input("Enter quantity to add: ").strip()
            if qty.isdigit():
                stock[item] = stock.get(item, 0) + int(qty)
                print(f"Updated '{item}' stock to {stock[item]}.")
                save_stock(filename, stock)  # Auto-save changes immediately
            else:
                print("Invalid quantity. Please enter a positive number.")

        elif choice == "2":
            if not stock:
                print("Stock is empty.")
                continue
            display_stock(stock)
            item = input("Enter item name to remove: ").strip().lower()
            if item in stock:
                qty = input("Enter quantity to remove: ").strip()
                if qty.isdigit() and int(qty) <= stock[item]:
                    stock[item] -= int(qty)
                    print(f"Updated '{item}' stock to {stock[item]}.")
                    save_stock(filename, stock)  # Auto-save changes immediately
                else:
                    print("Invalid quantity or not enough stock available.")
            else:
                print("Item not found in stock.")

        elif choice == "3":
            display_stock(stock)

        elif choice == "4":
            save_stock(filename, stock)
            break

        else:
            print("Invalid selection! Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()