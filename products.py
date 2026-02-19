# products.py
from storage import load_json, save_json

PRODUCTS_PATH = "data/products.json"

class ProductCatalog:
    def __init__(self):
        self.products = load_json(PRODUCTS_PATH, default=[])
        if not self.products:
            # Seed example products if file is empty (optional convenience)
            self.products = [
                {"product_id": "P1001", "name": "USB-C Cable", "price": 9.99, "stock": 30},
                {"product_id": "P1002", "name": "Wireless Mouse", "price": 19.99, "stock": 15},
            ]
            self._save()

    def _save(self):
        save_json(PRODUCTS_PATH, self.products)

    def list_all(self):
        return self.products

    def search(self, keyword: str):
        k = keyword.strip().lower()
        return [p for p in self.products if k in p["name"].lower()]

    def get_by_id(self, product_id: str):
        for p in self.products:
            if p["product_id"] == product_id:
                return p
        return None

    def deduct_stock(self, product_id: str, qty: int) -> bool:
        p = self.get_by_id(product_id)
        if not p or qty <= 0 or qty > p["stock"]:
            return False
        p["stock"] -= qty
        self._save()
        return True
