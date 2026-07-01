# helpers.py - Helper functions for main.py
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer


def display_menu() -> None:
    """
    Print the main menu of the GDPR data management system to the console.
    """
    print("========================================")
    print("      GDPR DATA MANAGEMENT SYSTEM       ")
    print("========================================")
    print("1) GDPR Art. 15: Access")
    print("2) GDPR Art. 17: Anonymization")
    print("3) Exit")
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