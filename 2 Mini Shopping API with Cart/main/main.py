from fastapi import FastAPI, HTTPException
from cart import add_to_cart, load_cart, calculate_checkout
from typing import List

app = FastAPI()


products = [
    {"id": 1, "name": "Laptop", "price": 599.99},
    {"id": 2, "name": "Smartphone", "price": 399.49},
    {"id": 3, "name": "Headphones", "price": 99.90},
]

@app.get("/products/")
def get_products():
    return products

@app.post("/cart/add")
def add_item_to_cart(product_id: int, qty: int):
    if qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    result = add_to_cart(product_id, qty, products)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Item added", "cart": result}

@app.get("/cart/checkout")
def checkout():
    cart = load_cart()
    return calculate_checkout(cart)
