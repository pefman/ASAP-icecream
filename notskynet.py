import sys
import os
import time
import random

def display_menu():
    menu = {
        "1": "Vanilla Scoop - $2.00",
        "2": "Chocolate Scoop - $2.50",
        "3": "Strawberry Scoop - $2.50",
        "4": "Waffle Cone - $1.00",
        "5": "Sprinkles - $0.50"
    }
    print("\n--- Ice Cream Parlor Menu ---")
    for key, item in menu.items():
        print(f"{key}. {item}")
    print("6. Checkout")
    return menu

def add_to_cart(cart, item_code, menu):
    if item_code in menu:
        cart.append(menu[item_code])
        print(f"Added: {menu[item_code]}")
        return True
    return False

def calculate_total(cart):
    total = 0.0
    for item in cart:
        try:
            total += float(item.split(" - $")[1])
        except ValueError:
            continue
    return total

def process_order(cart):
    total = calculate_total(cart)
    if total == 0:
        print("Cart is empty.")
        return False
    print(f"\nTotal Amount: ${total:.2f}")
    print("Processing payment (Simulation)...")
    time.sleep(1)
    print("Payment Successful.")
    print("Order Confirmed! Enjoy your ice cream.")
    return True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    cart = []
    print("Welcome to the Digital Ice Cream Simulator")
    print("Note: This is a simulation. No actual payment will be processed.")
    
    while True:
        clear_screen()
        menu = display_menu()
        choice = input("\nEnter item number or 6 to checkout: ").strip()
        
        if choice == "6":
            if process_order(cart):
                break
        elif choice in menu:
            add_to_cart(cart, choice, menu)
        else:
            print("Invalid choice.")
            time.sleep(1)
            clear_screen()
            
    print("\nThank you for visiting!")
    sys.exit(0)