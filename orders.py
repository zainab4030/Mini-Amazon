# orders.py
from datetime import datetime
from storage import load_json, save_json

ORDERS_PATH = "data/orders.json"

class OrderManager:
    def __init__(self):
        self.orders = load_json(ORDERS_PATH, default=[])

    def _save(self):
        save_json(ORDERS_PATH, self.orders)

    def _next_order_id(self) -> str:
        # O0001 format
        n = len(self.orders) + 1
        return f"O{n:04d}"

    def history_for_user(self, username: str):
        return [o for o in self.orders if o["username"] == username]

    def checkout(self, username: str, cart: dict, catalog) -> tuple[bool, str, dict | None]:
        if not cart:
            return False, "Cart is empty.", None

        # 1) re-validate stock
        for pid, qty in cart.items():
            p = catalog.get_by_id(pid)
            if not p:
                return False, f"Product {pid} not found.", None
            if qty > p["stock"]:
                return False, f"Not enough stock for {p['name']}.", None

        # 2) deduct stock
        items = []
        total = 0.0
        for pid, qty in cart.items():
            p = catalog.get_by_id(pid)
            catalog.deduct_stock(pid, qty)
            items.append({
                "product_id": pid,
                "name": p["name"],
                "qty": qty,
                "unit_price": p["price"],
                "subtotal": round(p["price"] * qty, 2)
            })
            total += p["price"] * qty

        # 3) receipt / order
        order = {
            "order_id": self._next_order_id(),
            "username": username,
            "items": [{"product_id": i["product_id"], "qty": i["qty"], "unit_price": i["unit_price"]} for i in items],
            "total": round(total, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.orders.append(order)
        self._save()
        

        receipt = {"order": order, "line_items": items}
        return True, "Checkout successful.", receipt
