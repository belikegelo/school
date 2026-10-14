import csv
import pharmacy


def test_search_medicine():
    """Verify that the search_medicine function works correctly."""
    inventory = [
        {"id": "1", "name": "Paracetamol", "variant": "500 mg",
         "price": 5.00, "quantity": 20},
        {"id": "2", "name": "Biogesic", "variant": "500 mg",
         "price": 6.00, "quantity": 15},
        {"id": "3", "name": "Paracetamol", "variant": "Syrup",
         "price": 50.00, "quantity": 10}
    ]

    assert len(pharmacy.search_medicine(inventory, "paracetamol")) == 2
    assert len(pharmacy.search_medicine(inventory, "500 mg")) == 2
    assert len(pharmacy.search_medicine(inventory, "BIOGESIC")) == 1
    assert pharmacy.search_medicine(inventory, "vitamins") == []


def test_get_product():
    """Verify that the get_product function works correctly."""
    inventory = [
        {"id": "1", "name": "Paracetamol", "variant": "500 mg",
         "price": 5.00, "quantity": 20},
        {"id": "2", "name": "Biogesic", "variant": "500 mg",
         "price": 6.00, "quantity": 15}
    ]

    assert pharmacy.get_product(inventory, "1") == inventory[0]
    assert pharmacy.get_product(inventory, "2") == inventory[1]
    assert pharmacy.get_product(inventory, "3") is None


def test_check_stock():
    """Verify that the check_stock function works correctly."""
    product = {
        "id": "1", "name": "Paracetamol", "variant": "500 mg",
        "price": 5.00, "quantity": 20
    }

    assert pharmacy.check_stock(product, 1) is True
    assert pharmacy.check_stock(product, 20) is True
    assert pharmacy.check_stock(product, 21) is False
    assert pharmacy.check_stock(product, 0) is False
    assert pharmacy.check_stock(product, -1) is False


def test_add_to_cart():
    """Verify that the add_to_cart function works correctly."""
    cart = []
    product = {
        "id": "1", "name": "Paracetamol", "variant": "500 mg",
        "price": 5.00, "quantity": 20
    }

    pharmacy.add_to_cart(cart, product, 3)

    assert len(cart) == 1
    assert cart[0] == {
        "name": "Paracetamol", "variant": "500 mg",
        "price": 5.00, "quantity": 3
    }


def test_calculate_item_total():
    """Verify that the calculate_item_total function works correctly."""
    assert pharmacy.calculate_item_total(5.00, 3) == 15.00
    assert pharmacy.calculate_item_total(12.50, 2) == 25.00
    assert pharmacy.calculate_item_total(8.00, 0) == 0.00


def test_calculate_cart_total():
    """Verify that the calculate_cart_total function works correctly."""
    cart = [
        {"name": "Paracetamol", "variant": "500 mg",
         "price": 5.00, "quantity": 3},
        {"name": "Biogesic", "variant": "500 mg",
         "price": 6.00, "quantity": 2}
    ]

    assert pharmacy.calculate_cart_total(cart) == 27.00
    assert pharmacy.calculate_cart_total([]) == 0


def test_update_stock():
    """Verify that the update_stock function works correctly."""
    product = {
        "id": "1", "name": "Paracetamol", "variant": "500 mg",
        "price": 5.00, "quantity": 20
    }

    pharmacy.update_stock(product, 5)
    assert product["quantity"] == 15

    pharmacy.update_stock(product, 3)
    assert product["quantity"] == 12


def test_load_inventory(tmp_path, monkeypatch):
    """Verify that the load_inventory function reads a CSV file."""
    filename = tmp_path / "inventory.csv"
    filename.write_text(
        "id,name,variant,price,quantity\n"
        "1,Paracetamol,500 mg,5.00,20\n"
        "2,Biogesic,500 mg,6.00,15\n",
        encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)

    inventory = pharmacy.load_inventory()

    assert len(inventory) == 2
    assert inventory[0]["name"] == "Paracetamol"
    assert inventory[0]["price"] == 5.00
    assert inventory[0]["quantity"] == 20
    assert inventory[1]["name"] == "Biogesic"


def test_load_inventory_file_not_found(tmp_path, monkeypatch, capsys):
    """Verify that load_inventory handles a missing CSV file."""
    monkeypatch.chdir(tmp_path)

    inventory = pharmacy.load_inventory()

    assert inventory is None
    assert "inventory.csv file not found" in capsys.readouterr().out


def test_save_inventory(tmp_path, monkeypatch):
    """Verify that the save_inventory function writes a CSV file."""
    monkeypatch.chdir(tmp_path)
    inventory = [
        {"id": "1", "name": "Paracetamol", "variant": "500 mg",
         "price": 5.00, "quantity": 15},
        {"id": "2", "name": "Biogesic", "variant": "500 mg",
         "price": 6.00, "quantity": 10}
    ]

    pharmacy.save_inventory(inventory)

    with open("inventory.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        saved_inventory = list(reader)

    assert len(saved_inventory) == 2
    assert saved_inventory[0]["name"] == "Paracetamol"
    assert float(saved_inventory[0]["price"]) == 5.00
    assert int(saved_inventory[0]["quantity"]) == 15
    assert saved_inventory[1]["name"] == "Biogesic"
    assert int(saved_inventory[1]["quantity"]) == 10


def test_show_search_results(capsys):
    """Verify that search results display medicine details and stock."""
    matches = [
        {"id": "1", "name": "Paracetamol", "variant": "500 mg",
         "price": 5.00, "quantity": 20},
        {"id": "2", "name": "Biogesic", "variant": "500 mg",
         "price": 6.00, "quantity": 0}
    ]

    pharmacy.show_search_results(matches)
    output = capsys.readouterr().out

    assert "Paracetamol - 500 mg" in output
    assert "₱5.00" in output
    assert "Stock: 20" in output
    assert "OUT OF STOCK" in output


def test_search_menu(capsys, monkeypatch):
    """Verify that search_menu displays matching medicines."""
    inventory = [
        {"id": "1", "name": "Paracetamol", "variant": "500 mg",
         "price": 5.00, "quantity": 20}
    ]
    monkeypatch.setattr("builtins.input", lambda prompt: "Paracetamol")

    pharmacy.search_menu(inventory)
    output = capsys.readouterr().out

    assert "Available Medicines:" in output
    assert "Paracetamol - 500 mg" in output


def test_search_menu_empty_input(capsys, monkeypatch):
    """Verify that search_menu handles an empty search term."""
    monkeypatch.setattr("builtins.input", lambda prompt: "   ")

    pharmacy.search_menu([])

    assert "Please enter a medicine name." in capsys.readouterr().out


def test_search_menu_no_match(capsys, monkeypatch):
    """Verify that search_menu handles a medicine that is not found."""
    monkeypatch.setattr("builtins.input", lambda prompt: "vitamins")

    pharmacy.search_menu([])

    assert "No medicine found." in capsys.readouterr().out


def test_print_receipt(capsys):
    """Verify that print_receipt displays the items and cart total."""
    cart = [
        {"name": "Paracetamol", "variant": "500 mg",
         "price": 5.00, "quantity": 3},
        {"name": "Biogesic", "variant": "500 mg",
         "price": 6.00, "quantity": 2}
    ]

    pharmacy.print_receipt(cart)
    output = capsys.readouterr().out

    assert "RECEIPT" in output
    assert "3 x Paracetamol - 500 mg" in output
    assert "2 x Biogesic - 500 mg" in output
    assert "TOTAL: ₱27.00" in output
    assert "Thank you!" in output


def test_show_menu(capsys):
    """Verify that show_menu displays the main menu options."""
    pharmacy.show_menu()
    output = capsys.readouterr().out

    assert "1. Search Medicine" in output
    assert "2. Buy Medicine" in output
    assert "3. Exit" in output


def test_buy_medicine(tmp_path, monkeypatch, capsys):
    """Verify that buying medicine updates stock and saves the inventory."""
    monkeypatch.chdir(tmp_path)
    inventory = [
        {"id": "1", "name": "Paracetamol", "variant": "500 mg",
         "price": 5.00, "quantity": 10}
    ]
    answers = iter(["Paracetamol", "1", "2", "2"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    pharmacy.buy_medicine(inventory)

    output = capsys.readouterr().out
    assert inventory[0]["quantity"] == 8
    assert "Added to cart:" in output
    assert "Item total: ₱10.00" in output
    assert "TOTAL: ₱10.00" in output

    with open("inventory.csv", "r", newline="", encoding="utf-8") as file:
        saved_inventory = list(csv.DictReader(file))

    assert int(saved_inventory[0]["quantity"]) == 8
