import json
from math import ceil

CART_FILE = "cart.json"

def load_cart():
    try:
        with open(CART_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cart(cart):
    with open(CART_FILE, "w") as f:
        json.dump(cart, f, indent=4)

def add_to_cart(product_id: int, quantity: int, product_catalog: list):
    cart = load_cart()
    product = next((p for p in product_catalog if p["id"] == product_id), None)
    if not product:
        return None
    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += quantity
    else:
        cart[str(product_id)] = {
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity
        }
    save_cart(cart)
    return cart

def calculate_checkout(cart):
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return {"total": ceil(total), "items": cart}
