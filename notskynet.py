import json
import random
from datetime import datetime

class IceCreamFlavor:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"{self.name} (${self.price})"

class IceCreamShop:
    def __init__(self, name):
        self.name = name
        self.flavors = [
            IceCreamFlavor("Vanilla", 2.00, 10),
            IceCreamFlavor("Chocolate", 2.50, 10),
            IceCreamFlavor("Strawberry", 3.00, 5),
            IceCreamFlavor("Mint Chip", 3.50, 8)
        ]

    def get_menu(self):
        return self.flavors

    def check_availability(self, flavor_name):
        for flavor in self.flavors:
            if flavor.name == flavor_name:
                return flavor.stock > 0
        return False

class Order:
    def __init__(self, shop, customer_name):
        self.shop = shop
        self.customer_name = customer_name
        self.items = []
        self.total_cost = 0.0
        self.promo_code = None
        self.is_free = False

    def add_item(self, flavor_name, quantity=1):
        for flavor in self.shop.get_menu():
            if flavor.name == flavor_name and flavor.stock >= quantity:
                self.items.append((flavor, quantity))
                self.total_cost += flavor.price * quantity
                flavor.stock -= quantity
                return True
        return False

    def apply_promo(self, code):
        if code == "FREEICECREAM2024":
            self.is_free = True
            self.promo_code = code
            self.total_cost = 0.0
            return True
        return False

    def process_payment(self):
        if self.is_free:
            return "Payment waived via promo code."
        elif self.total_cost > 0:
            return f"Processing payment for ${self.total_cost:.2f}..."
        return "No items added."

    def confirm_order(self):
        return {
            "order_id": f"ORD-{random.randint(1000, 9999)}",
            "shop": self.shop.name,
            "customer": self.customer_name,
            "items": [f"{qty}x {name}" for name, qty in [(f.name, q) for f, q in self.items]],
            "total_paid": f"${self.total_cost:.2f}",
            "status": "CONFIRMED",
            "timestamp": datetime.now().isoformat(),
            "simulation_note": "This is a mock ordering system. No real money or goods are exchanged."
        }

def run_simulation():
    shop = IceCreamShop("Sweet Treats")
    user = Order(shop, "Demo User")

    print("Welcome to Sweet Treats Online Ordering System.")
    print("Menu:")
    for flavor in shop.get_menu():
        print(f"  - {flavor}")

    print("\nAdding Vanilla (1 scoop) and Chocolate (1 scoop)...")
    user.add_item("Vanilla")
    user.add_item("Chocolate")

    print("\nApplying free promo code...")
    user.apply_promo("FREEICECREAM2024")

    print("\nProcessing Order...")
    payment_status = user.process_payment()
    order_details = user.confirm_order()

    print("\n--- Order Confirmation ---")
    print(f"Order ID: {order_details['order_id']}")
    print(f"Items: {', '.join(order_details['items'])}")
    print(f"Total Paid: {order_details['total_paid']}")
    print(f"Payment Status: {payment_status}")
    print(f"Note: {order_details['simulation_note']}")

    return order_details

if __name__ == "__main__":
    run_simulation()