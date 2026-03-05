import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class IceCreamFlavor:
    name: str
    price: float
    stock: int

@dataclass
class OrderItem:
    flavor: IceCreamFlavor
    quantity: int

@dataclass
class Order:
    order_id: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"

class IceCreamShop:
    def __init__(self):
        self.menu: Dict[str, IceCreamFlavor] = {
            "vanilla": IceCreamFlavor(name="Vanilla", price=3.50, stock=100),
            "chocolate": IceCreamFlavor(name="Chocolate", price=4.00, stock=80),
            "strawberry": IceCreamFlavor(name="Strawberry", price=4.50, stock=60),
            "mint_chip": IceCreamFlavor(name="Mint Chip", price=4.50, stock=50),
            "cookie_dough": IceCreamFlavor(name="Cookie Dough", price=5.00, stock=40),
        }
        self.active_orders: List[Order] = []

    def get_menu(self) -> Dict[str, Dict]:
        return {k: {"price": v.price, "stock": v.stock} for k, v in self.menu.items()}

    def add_to_cart(self, flavor_key: str, quantity: int) -> Optional[str]:
        if flavor_key not in self.menu:
            return "Flavor not found"
        flavor = self.menu[flavor_key]
        if flavor.stock < quantity:
            return f"Insufficient stock for {flavor.name}"
        return f"Added {quantity} {flavor.name} to cart"

    def create_order(self, customer_id: str) -> Optional[Order]:
        if not hasattr(self, 'cart') or not self.cart:
            return None
        order_id = str(uuid.uuid4())
        items = []
        total = 0.0
        for item in self.cart:
            flavor = self.menu[item.flavor]
            if flavor.stock >= item.quantity:
                items.append(item)
                total += flavor.price * item.quantity
                flavor.stock -= item.quantity
            else:
                return None
        order = Order(order_id=order_id, items=items, total_amount=total)
        order.status = "processing"
        self.active_orders.append(order)
        return order

    def process_payment(self, order: Order, payment_method: str) -> bool:
        if order.total_amount <= 0:
            return False
        if payment_method not in ["credit_card", "debit_card", "digital_wallet"]:
            return False
        time.sleep(0.5)
        order.status = "paid"
        return True

    def fulfill_order(self, order: Order) -> bool:
        if order.status != "paid":
            return False
        order.status = "fulfilled"
        return True

    def cancel_order(self, order_id: str) -> bool:
        for order in self.active_orders:
            if order.order_id == order_id and order.status in ["pending", "processing"]:
                order.status = "cancelled"
                for item in order.items:
                    self.menu[item.flavor].stock += item.quantity
                return True
        return False

def main():
    shop = IceCreamShop()
    shop.cart = []
    
    cart_flavors = [
        ("vanilla", 2),
        ("chocolate", 1),
    ]
    
    for flavor_key, quantity in cart_flavors:
        print(shop.add_to_cart(flavor_key, quantity))
    
    order = shop.create_order("customer_123")
    
    if order:
        print(f"Order created: {order.order_id}")
        print(f"Total amount: ${order.total_amount:.2f}")
        
        if shop.process_payment(order, "credit_card"):
            print("Payment processed successfully")
            if shop.fulfill_order(order):
                print("Order fulfilled")
                print(f"Order Status: {order.status}")
            else:
                print("Failed to fulfill order")
        else:
            print("Payment failed")
    else:
        print("Order creation failed")

if __name__ == "__main__":
    main()