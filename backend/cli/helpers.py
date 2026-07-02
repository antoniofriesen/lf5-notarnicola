# helpers.py - Helper functions for main.py
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer


def display_menu() -> None:
    """
    Print the main menu of the GDPR data management system to the console.
    """
    print("========================================")
    print("      NOTARNICOLA DATA MANAGEMENT SYSTEM       ")
    print("========================================")
    print("1) GDPR")
    print("2) Customers")
    print("3) Orders")
    print("4) Products")
    print("5) Exit")
    print("========================================")


def display_gdpr_menu() -> None:
    """
    Print the gdpr menu of the Notarnicola data management system to the console.
    """
    print("========================================")
    print("      NOTARNICOLA DATA MANAGEMENT SYSTEM       ")
    print("========================================")
    print("-> GDPR MENU <-")
    print("1) GDPR Art. 15: Access")
    print("2) GDPR Art. 17: Anonymization")
    print("3) Back")
    print("========================================")


def display_customer_menu() -> None:
    """
    Print the customer menu of the Notarnicola data management system to the console.
    """
    print("========================================")
    print("      NOTARNICOLA DATA MANAGEMENT SYSTEM       ")
    print("========================================")
    print("-> CUSTOMER MENU <-")
    print("1) Create new customer")
    print("2) Get all customer data")
    print("3) Update customer")
    print("4) Anonymize customer")
    print("5) Back")
    print("========================================")


def display_order_menu() -> None:
    """
    Print the order menu of the Notarnicola data management system to the console.
    """
    print("========================================")
    print("      NOTARNICOLA DATA MANAGEMENT SYSTEM       ")
    print("========================================")
    print("-> ORDER MENU <-")
    print("1) Create new order")
    print("2) Get all order data")
    print("3) Update order")
    print("4) Cancel order")
    print("5) Back")
    print("========================================")


def display_product_menu() -> None:
    """
    Print the product menu of the Notarnicola data management system to the console.
    """
    print("========================================")
    print("      NOTARNICOLA DATA MANAGEMENT SYSTEM       ")
    print("========================================")
    print("-> PRODUCT MENU <-")
    print("1) Create new product")
    print("2) Get all product data")
    print("3) Update product")
    print("4) Deactivate product")
    print("5) Back")
    print("========================================")


def get_valid_customer_id() -> int:
    """
    Prompt the user to enter a valid customer ID and return it as an integer.

    Loops indefinitely until the user provides a valid positive integer.
    Whitespace is stripped from the input before validation.

    Returns:
        int: a valid positive customer ID entered by the user.
    """
    while True:
        user_input = input("Please enter a Customer ID: ").strip()

        if user_input.isdigit() and int(user_input) > 0:
            return int(user_input)

        print("Error: Invalid input. Customer ID must be a positive number.")