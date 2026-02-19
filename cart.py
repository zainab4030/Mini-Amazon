# cart.py
from storage import load_json, save_json

CARTS_PATH = "data/carts.json"

class CartManager:
    def __init__(self):
        # Structure: { "alice": { "P1002": 2, "P1001": 1 }, ... }
        self.carts = load_json(CARTS_PATH, default={})

    def _save(self):
        save_json(CARTS_PATH, self.carts)

    def get_cart(self, username: str) -> dict:
        return self.carts.get(username, {})

    def add_item(self, username: str, product_id: str, qty: int, available_stock: int) -> tuple[bool, str]:
        if qty <= 0:
            return False, "Quantity must be greater than zero."
        cart = self.carts.setdefault(username, {})
        current = cart.get(product_id, 0)
        if current + qty > available_stock:
            return False, "Cannot add more than available stock."
        cart[product_id] = current + qty
        self._save()
        return True, "Item added to cart."

    def remove_item(self, username: str, product_id: str, qty: int | None = None) -> tuple[bool, str]:
        cart = self.carts.get(username, {})
        if product_id not in cart:
            return False, "Item not in cart."
        if qty is None or qty >= cart[product_id]:
            del cart[product_id]
        else:
            if qty <= 0:
                return False, "Quantity must be greater than zero."
            cart[product_id] -= qty
        self.carts[username] = cart
        self._save()
        return True, "Cart updated."

    def clear_cart(self, username: str) -> None:
        self.carts[username] = {}
        self._save()
