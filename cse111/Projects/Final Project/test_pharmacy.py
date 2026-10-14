import pytest
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
    assert len(pharmacy.search_medicine(inventory, "biogesic")) == 1
    assert len(pharmacy.search_medicine(inventory, "vitamins")) == 0


def test_check_stock():
    """Verify that the check_stock function works correctly."""
    product = {
        "id": "1",
        "name": "Paracetamol",
        "variant": "500 mg",
        "price": 5.00,
        "quantity": 20
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
        "id": "1",
        "name": "Paracetamol",
        "variant": "500 mg",
        "price": 5.00,
        "quantity": 20
    }

    pharmacy.add_to_cart(cart, product, 3)

    assert len(cart) == 1
    assert cart[0]["name"] == "Paracetamol"
    assert cart[0]["variant"] == "500 mg"
    assert cart[0]["price"] == 5.00
    assert cart[0]["quantity"] == 3


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


if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
