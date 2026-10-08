import csv
import datetime


def load_inventory():
    """Read the inventory from the CSV file and return it as a list."""
    inventory = []

    with open("inventory.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["price"] = float(row["price"])
            row["quantity"] = int(row["quantity"])
            inventory.append(row)

    return inventory


def save_inventory(inventory):
    """Save the current inventory back to the CSV file."""
    with open("inventory.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "name", "variant", "price", "quantity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for product in inventory:
            writer.writerow(product)


def search_medicine(inventory, search_term):
    """Return products whose name or variant matches the search term."""
    matches = []
    search_term = search_term.lower()

    for product in inventory:
        name = product["name"].lower()
        variant = product["variant"].lower()

        if search_term in name or search_term in variant:
            matches.append(product)

    return matches


def get_product(inventory, product_id):
    """Return a product with the given ID."""
    for product in inventory:
        if product["id"] == product_id:
            return product

    return None


def check_stock(product, quantity):
    """Return True if the requested quantity is available."""
    return quantity > 0 and quantity <= product["quantity"]


def add_to_cart(cart, product, quantity):
    """Add a product and quantity to the cart."""
    cart_item = {
        "name": product["name"],
        "variant": product["variant"],
        "price": product["price"],
        "quantity": quantity
    }

    cart.append(cart_item)


def calculate_item_total(price, quantity):
    """Calculate the total price for one item."""
    return price * quantity


def calculate_cart_total(cart):
    """Calculate the total price of everything in the cart."""
    total = 0

    for item in cart:
        total += calculate_item_total(
            item["price"],
            item["quantity"]
        )

    return total


def update_stock(product, quantity):
    """Reduce the product stock after a purchase."""
    product["quantity"] -= quantity


def print_receipt(cart):
    """Print the receipt for the purchase."""
    current_time = datetime.datetime.now()

    print("\n")
    print("=" * 40)
    print("              RECEIPT")
    print("=" * 40)
    print(
        current_time.strftime("%B %d, %Y - %I:%M %p")
    )
    print("-" * 40)

    for item in cart:
        item_total = calculate_item_total(
            item["price"],
            item["quantity"]
        )

        print(
            f'{item["quantity"]} x '
            f'{item["name"]} - {item["variant"]}'
        )
        print(f'   ₱{item["price"]:.2f} each = ₱{item_total:.2f}')

    total = calculate_cart_total(cart)

    print("-" * 40)
    print(f"TOTAL: ₱{total:.2f}")
    print("=" * 40)
    print("Thank you!")
    print("=" * 40)


def show_search_results(matches):
    """Display search results."""
    print("\nAvailable Medicines:")
    print("-" * 60)

    for index, product in enumerate(matches, start=1):
        if product["quantity"] > 0:
            stock_text = f"Stock: {product['quantity']}"
        else:
            stock_text = "OUT OF STOCK"

        print(
            f"{index}. "
            f"{product['name']} - "
            f"{product['variant']} | "
            f"₱{product['price']:.2f} | "
            f"{stock_text}"
        )

    print("-" * 60)


def search_menu(inventory):
    """Search for medicine and display the available stock."""
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
    """Handle the buying process."""
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

        add_to_cart(cart, selected_product, quantity)
        update_stock(selected_product, quantity)

        item_total = calculate_item_total(
            selected_product["price"],
            quantity
        )

        print("\nAdded to cart:")
        print(
            f'{quantity} x '
            f'{selected_product["name"]} - '
            f'{selected_product["variant"]}'
        )
        print(f"Item total: ₱{item_total:.2f}")

        while True:
            print("\nBuy another medicine?")
            print("1. Yes")
            print("2. No")

            again = input("Choose: ")

            if again == "1":
                break

            if again == "2":
                print_receipt(cart)
                save_inventory(inventory)
                return

            print("Please choose 1 or 2.")


def show_menu():
    """Display the main menu."""
    print("\n")
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

    print("Welcome to the Inventory Management System")

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