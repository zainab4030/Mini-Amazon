# main.py
from users import UserManager
from products import ProductCatalog
from cart import CartManager
from orders import OrderManager

def prompt_int(msg: str) -> int | None:
    try:
        return int(input(msg).strip())
    except ValueError:
        return None

def welcome_menu():
    users = UserManager()
    catalog = ProductCatalog()
    carts = CartManager()
    orders = OrderManager()

    while True:
        print("\n=== WELCOME MENU ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            u = input("Username: ")
            p = input("Password (min 6 chars): ")
            ok, msg = users.register(u, p)
            print(msg)

        elif choice == "2":
            u = input("Username: ").strip()
            p = input("Password: ").strip()
            if users.authenticate(u, p):
                print("Login successful.")
                store_menu(u, catalog, carts, orders)
            else:
                print("Invalid username or password.")

        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")

def store_menu(username, catalog, carts, orders):
    while True:
        print(f"\n=== STORE MENU (User: {username}) ===")
        print("1. Browse products")
        print("2. Search products")
        print("3. View cart")
        print("4. Checkout")
        print("5. View order history")
        print("6. Logout")
        choice = input("Choose: ").strip()

        if choice == "1":
            for p in catalog.list_all():
                print(f"{p['product_id']} | {p['name']} | €{p['price']} | Stock: {p['stock']}")
            pid = input("Enter product id to add (or blank to return): ").strip()
            if pid:
                product = catalog.get_by_id(pid)
                if not product:
                    print("Product not found.")
                    continue
                qty = prompt_int("Quantity: ")
                if qty is None:
                    print("Invalid quantity.")
                    continue
                ok, msg = carts.add_item(username, pid, qty, available_stock=product["stock"])
                print(msg)

        elif choice == "2":
            kw = input("Keyword: ")
            results = catalog.search(kw)
            if not results:
                print("No products found.")
            else:
                for p in results:
                    print(f"{p['product_id']} | {p['name']} | €{p['price']} | Stock: {p['stock']}")

        elif choice == "3":
            cart = carts.get_cart(username)
            if not cart:
                print("Cart is empty.")
                continue
            total = 0.0
            print("Items:")
            for pid, qty in cart.items():
                p = catalog.get_by_id(pid)
                if not p:
                    continue
                subtotal = p["price"] * qty
                total += subtotal
                print(f"- {p['name']} | Qty: {qty} | Unit: €{p['price']} | Subtotal: €{subtotal:.2f}")
            print(f"Total: €{total:.2f}")

            pid = input("Enter product id to remove (or blank to return): ").strip()
            if pid:
                qtxt = input("Quantity to remove (blank = remove all): ").strip()
                qty = None if qtxt == "" else int(qtxt) if qtxt.isdigit() else -1
                if qty == -1:
                    print("Invalid quantity.")
                else:
                    ok, msg = carts.remove_item(username, pid, qty)
                    print(msg)

        elif choice == "4":
            cart = carts.get_cart(username)
            ok, msg, receipt = orders.checkout(username, cart, catalog)
            print(msg)
            if ok:
                carts.clear_cart(username)
                o = receipt["order"]
                print("\n=== RECEIPT ===")
                print(f"Order ID: {o['order_id']}")
                print(f"Username: {o['username']}")
                print(f"Date/Time: {o['timestamp']}")
                print("Items purchased:")
                for it in receipt["line_items"]:
                    print(f"- {it['name']} | Qty: {it['qty']} | Unit: €{it['unit_price']:.2f}")
                print(f"Total cost: €{o['total']:.2f}")

        elif choice == "5":
            hist = orders.history_for_user(username)
            if not hist:
                print("No orders yet.")
            else:
                for o in hist:
                    print(f"{o['order_id']} | Total: €{o['total']} | {o['timestamp']}")

        elif choice == "6":
            print("Logged out.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    welcome_menu()))
