import sys


def load_stock(filename: str) -> dict[str, int]:  "read the stock file"
    
    stock = {}
    try:
        with open(filename, "r") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 2:
                    raise ValueError(f"Corrupted format on line {line_num}: '{line}'")
                item, count = parts[0].strip().lower(), parts[1].strip()
                stock[item] = int(count)
        return stock
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def display_stock(stock: dict[str, int]) -> list[str]:  "print stock and returns ordered item list using pointers."
   
    items = list(stock.keys())
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}: {stock[item]}")
    return items


def select_stock_item(stock: dict[str, int], items: list[str], allow_new: bool = True) -> str | None:  "checking input."
    
    prompt = f'Enter stock name or ID (1-{len(items)}): '
    user_input = input(prompt).strip().lower()

    if user_input.isdigit():
        idx = int(user_input)
        if 1 <= idx <= len(items):
            return items[idx - 1]
        else:
            print("Invalid numeric ID.")
            return None
    elif user_input:
        if not allow_new and user_input not in stock:
            print(f"Item '{user_input}' not in stock.")
            return None
        return user_input
    else:
        print("Input cannot be empty.")
        return None


def add_stock(stock: dict[str, int]) -> None:
    items = display_stock(stock)
    item = select_stock_item(stock, items, allow_new=True)
    if not item:
        return

    qty_str = input(f"Enter amount to add to '{item}': ").strip()
    if not qty_str.isdigit() or int(qty_str) < 0:
        print("Invalid quantity. Must be a non-negative integer.")
        return

    quantity = int(qty_str)
    stock[item] = stock.get(item, 0) + quantity
    print(f"Successfully updated '{item}' stock to {stock[item]}.")


def remove_stock(stock: dict[str, int]) -> None:
    if not stock:
        print("Stock is empty.")
        return

    items = display_stock(stock)
    item = select_stock_item(stock, items, allow_new=False)
    if not item:
        return

    qty_str = input(f"Enter amount to remove from '{item}': ").strip()
    if not qty_str.isdigit() or int(qty_str) < 0:
        print("Invalid quantity. Must be a non-negative integer.")
        return

    quantity = int(qty_str)
    if stock[item] - quantity < 0:
        print(f"Error: Removing {quantity} would result in negative stock ({stock[item]} available).")
        return

    stock[item] -= quantity
    print(f"Successfully updated '{item}' stock to {stock[item]}.")


def save_stock(filename: str, stock: dict[str, int]) -> None:
    try:
        with open(filename, "w") as file:
            for item, quantity in stock.items():
                file.write(f"{item},{quantity}\n")
        print("Stock changes saved successfully. Exiting program.")
    except IOError as e:
        print(f"Error saving file: {e}")


def main():
    filename = "stock.txt"
    stock = load_stock(filename)

    while True:
        print("\n--- Stock Manager Menu ---")
        print("enter 1 to add stock")
        print("enter 2 to remove stock")
        print("enter 3 to show stock's contents")
        print("enter 4 to exit the program")

        choice = input("Enter option (1-4): ").strip()

        if choice == "1":
            add_stock(stock)
        elif choice == "2":
            remove_stock(stock)
        elif choice == "3":
            display_stock(stock)
        elif choice == "4":
            save_stock(filename, stock)
            break
        else:
            print("Invalid selection! Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
