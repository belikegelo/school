import csv
from datetime import datetime


def load_inventory():
    """Read the inventory from the CSV file."""
    inventory = []

    try:
        with open("inventory.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                row["price"] = float(row["price"])
                row["quantity"] = int(row["quantity"])
                inventory.append(row)

        return inventory

    except FileNotFoundError:
        print("Error: inventory.csv file not found.")
        return None


def save_inventory(inventory):
    """Save the updated inventory to the CSV file."""
    with open("inventory.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "name", "variant", "price", "quantity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for product in inventory:
            writer.writerow(product)


def search_medicine(inventory, search_term):
    """Search for a medicine by its name or variant."""
    matches = []
    search_term = search_term.lower()

    for product in inventory:
        name = product["name"].lower()
        variant = product["variant"].lower()

        if search_term in name or search_term in variant:
            matches.append(product)

    return matches


def get_product(inventory, product_id):
    """Find a product using its ID."""
    for product in inventory:
        if product["id"] == product_id:
            return product

    return None


def check_stock(product, quantity):
    """Check if the requested quantity is available."""
    if quantity > 0 and quantity <= product["quantity"]:
        return True

    return False


def add_to_cart(cart, product, quantity):
    """Add the selected medicine to the cart."""
    cart_item = {
        "name": product["name"],
        "variant": product["variant"],
        "price": product["price"],
        "quantity": quantity
    }

    cart.append(cart_item)


def calculate_item_total(price, quantity):
    """Calculate the total price of one medicine."""
    total = price * quantity
    return total


def calculate_cart_total(cart):
    """Calculate the total price of all medicines in the cart."""
    total = 0

    for item in cart:
        item_total = calculate_item_total(
            item["price"],
            item["quantity"]
        )
        total += item_total

    return total


def update_stock(product, quantity):
    """Reduce the stock after buying a medicine."""
    product["quantity"] -= quantity


def print_receipt(cart):
    """Print the receipt after purchasing medicines."""
    current_time = datetime.now()

    print()
    print("=" * 40)
    print("              RECEIPT")
    print("=" * 40)
    print(current_time.strftime("%B %d, %Y - %I:%M %p"))
    print("-" * 40)

    for item in cart:
        item_total = calculate_item_total(
            item["price"],
            item["quantity"]
        )

        print(f'{item["quantity"]} x {item["name"]} - {item["variant"]}')
        print(f'   ₱{item["price"]:.2f} each = ₱{item_total:.2f}')

    total = calculate_cart_total(cart)

    print("-" * 40)
    print(f"TOTAL: ₱{total:.2f}")
    print("=" * 40)
    print("Thank you!")
    print("=" * 40)


def show_search_results(matches):
    """Display the search results and available stock."""
    print()
    print("Available Medicines:")
    print("-" * 60)

    for index, product in enumerate(matches, start=1):
        if product["quantity"] > 0:
            stock_text = f"Stock: {product['quantity']}"
        else:
            stock_text = "OUT OF STOCK"

        print(
            f"{index}. {product['name']} - {product['variant']} | "
            f"₱{product['price']:.2f} | {stock_text}"
        )

    print("-" * 60)


def search_menu(inventory):
    """Allow the user to search for a medicine."""
    search_term = input("\nEnter medicine to search: ").strip()

    if search_term == "":
        print("Please enter a medicine name.")
        return

    matches = search_medicine(inventory, search_term)

    if len(matches) == 0:
        print("No medicine found.")
        return

    show_search_results(matches)


def buy_medicine(inventory):
    """Handle the process of buying medicines."""
    cart = []

    while True:
        search_term = input("\nEnter medicine to buy: ").strip()

        if search_term == "":
            print("Please enter a medicine name.")
            continue

        matches = search_medicine(inventory, search_term)

        if len(matches) == 0:
            print("No medicine found.")
            continue

        show_search_results(matches)

        # Ask the user to choose a medicine
        while True:
            try:
                choice = int(input("Choose a medicine number: "))

                if choice < 1 or choice > len(matches):
                    print("Invalid choice.")
                    continue

                break

            except ValueError:
                print("Please enter a number.")

        selected_product = matches[choice - 1]

        if selected_product["quantity"] == 0:
            print("Sorry, this product is out of stock.")
            continue

        # Ask for the quantity
        while True:
            try:
                quantity = int(
                    input(
                        f"Enter quantity "
                        f"(Available: {selected_product['quantity']}): "
                    )
                )

                if check_stock(selected_product, quantity):
                    break

                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                else:
                    print(
                        f"Not enough stock. "
                        f"Available: {selected_product['quantity']}"
                    )

            except ValueError:
                print("Please enter a whole number.")

        # Add the medicine to the cart and update stock
        add_to_cart(cart, selected_product, quantity)
        update_stock(selected_product, quantity)

        item_total = calculate_item_total(
            selected_product["price"],
            quantity
        )

        print("\nAdded to cart:")
        print(
            f'{quantity} x {selected_product["name"]} - '
            f'{selected_product["variant"]}'
        )
        print(f"Item total: ₱{item_total:.2f}")

        # Ask if the user wants to buy another medicine
        while True:
            print("\nBuy another medicine?")
            print("1. Yes")
            print("2. No")

            again = input("Choose: ")

            if again == "1":
                break

            elif again == "2":
                print_receipt(cart)
                save_inventory(inventory)
                return

            else:
                print("Please choose 1 or 2.")


def show_menu():
    """Display the main menu."""
    print()
    print("=" * 40)
    print("       MINI PHARMACY SYSTEM")
    print("=" * 40)
    print("1. Search Medicine")
    print("2. Buy Medicine")
    print("3. Exit")
    print("=" * 40)


def main():
    """Run the pharmacy inventory system."""
    inventory = load_inventory()

    if inventory is None:
        return

    print()
    print("Welcome to GELO's Inventory Management System")

    while True:
        show_menu()

        choice = input("Choose an option: ")

        if choice == "1":
            search_menu(inventory)

        elif choice == "2":
            buy_medicine(inventory)

        elif choice == "3":
            print("\nThank you for using the system!")
            break

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()