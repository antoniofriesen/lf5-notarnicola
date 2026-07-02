# main.py - Central entry point for Notarnicola Data Management System
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

from decimal import Decimal

from backend.db.db_utils import connect_2_db, close_db_connection
from backend.cli.helpers import (
    display_menu,
    display_gdpr_menu,
    display_customer_menu,
    display_order_menu,
    display_product_menu,
    get_valid_customer_id,
)
from backend.models.customers import (
    get_customer_master_data,
    get_customer_orders,
    get_customer_order_positions,
    create_customer,
    update_customer,
    anonymize_customer,
)
from backend.models.orders import (
    create_order,
    get_all_orders,
    get_order_by_id,
    update_order,
    cancel_order,
)
from backend.models.products import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    deactivate_product,
)
from backend.models.locations import get_or_create_location
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


# ─── GDPR HANDLERS ────────────────────────────────────────────────────────────

def handle_access(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """
    Handle a GDPR Art. 15 access request.

    Prompts the user for a customer ID, retrieves and displays all
    stored personal data for that customer, including master data,
    orders, and order positions.

    Args:
        connection (MySQLConnectionAbstract | PooledMySQLConnection):
            an active database connection.
    """
    print("Enter Customer ID:")
    customer_id = get_valid_customer_id()

    print("Searching for Customer ID...")
    master_data = get_customer_master_data(customer_id, connection)

    if not master_data:
        print("Validation Error: Customer with ID does not exist.")
        return

    orders = get_customer_orders(customer_id, connection)
    positions = get_customer_order_positions(customer_id, connection)

    print("--- [ CUSTOMER MASTER DATA ] ---")
    for row in master_data:
        print(f"  First Name:   {row[0]}")
        print(f"  Last Name:    {row[1]}")
        print(f"  Street:       {row[2]}")
        print(f"  House Number: {row[3]}")
        print(f"  Postal Code:  {row[4]}")
        print(f"  City:         {row[5]}")

    print("\n--- [ CUSTOMER ORDERS ] ---")
    for row in orders:
        print(f"  Order #{row[0]}")
        print(f"    Date:    {row[2].strftime('%d.%m.%Y')}")
        print(f"    Amount:  {row[1]} €")

    print("\n--- [ CUSTOMER ORDER POSITIONS ] ---")
    for i, row in enumerate(positions, start=1):
        print(f"  Position #{i}")
        print(f"    Product:  {row[3]}")
        print(f"    Unit:     {row[4] if row[4] else '-'}")
        print(f"    Price:    {row[5]} €")
        print(f"    Quantity: {row[6]}")


def handle_anonymization(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """
    Handle a GDPR Art. 17 erasure request via pseudonymization.

    Args:
        connection (MySQLConnectionAbstract | PooledMySQLConnection):
            an active database connection.
    """
    print("Enter Customer ID to anonymize:")
    customer_id = get_valid_customer_id()

    print("Searching for Customer ID...")
    master_data = get_customer_master_data(customer_id, connection)

    if not master_data:
        print("Validation Error: Anonymization impossible. Customer ID does not exist.")
        return

    print("WARNING: You are about to permanently anonymize this customer!")

    while True:
        print("Are you absolutely sure? (yes/no):")
        confirmation = input().strip().lower()

        if confirmation in ["yes", "y", "ja", "j"]:
            success = anonymize_customer(customer_id, connection)
            if not success:
                print("Error: Could not anonymize customer. Operation aborted.")
                return
            print("Success: Customer personal data has been anonymized.")
            return

        elif confirmation in ["no", "n", "nein"]:
            print("Anonymization canceled by user.")
            return

        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


# ─── CUSTOMER HANDLERS ────────────────────────────────────────────────────────

def handle_create_customer(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for customer data and create a new customer."""
    print("--- [ CREATE CUSTOMER ] ---")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    street = input("Street: ").strip()
    house_number = input("House Number: ").strip()

    plz = input("Postal Code: ").strip()
    city = input("City: ").strip()
    ort_id = get_or_create_location(plz, city, connection)

    if ort_id is None:
        print("Error: Could not resolve location.")
        return

    create_customer(first_name, last_name, street, house_number, ort_id, connection)


def handle_get_customer(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for a customer ID and display all customer data."""
    print("Enter Customer ID:")
    customer_id = get_valid_customer_id()
    master_data = get_customer_master_data(customer_id, connection)

    if not master_data:
        print("Validation Error: Customer with ID does not exist.")
        return

    print("--- [ CUSTOMER DATA ] ---")
    for row in master_data:
        print(f"  First Name:   {row[0]}")
        print(f"  Last Name:    {row[1]}")
        print(f"  Street:       {row[2]}")
        print(f"  House Number: {row[3]}")
        print(f"  Postal Code:  {row[4]}")
        print(f"  City:         {row[5]}")


def handle_update_customer(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for a customer ID and updated data, then update the customer."""
    print("Enter Customer ID to update:")
    customer_id = get_valid_customer_id()

    master_data = get_customer_master_data(customer_id, connection)
    if not master_data:
        print("Validation Error: Customer with ID does not exist.")
        return

    print("--- [ UPDATE CUSTOMER ] ---")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    street = input("Street: ").strip()
    house_number = input("House Number: ").strip()

    plz = input("Postal Code: ").strip()
    city = input("City: ").strip()
    ort_id = get_or_create_location(plz, city, connection)

    if ort_id is None:
        print("Error: Could not resolve location.")
        return

    update_customer(customer_id, first_name, last_name, street, house_number, ort_id, connection)


# ─── ORDER HANDLERS ───────────────────────────────────────────────────────────

def handle_create_order(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for order data and create a new order."""
    print("--- [ CREATE ORDER ] ---")
    print("Enter Customer ID:")
    customer_id = get_valid_customer_id()

    try:
        amount = Decimal(input("Amount (€): ").strip())
    except Exception:
        print("Error: Amount must be a valid number.")
        return

    create_order(customer_id, amount, connection)


def handle_get_orders(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Display all orders or a specific order by ID."""
    print("--- [ ORDERS ] ---")
    orders = get_all_orders(connection)

    if not orders:
        print("No orders found.")
        return

    for row in orders:
        status = "CANCELLED" if row[4] else "ACTIVE"
        print(f"  Order #{row[0]} | Customer {row[1]} | {row[2].strftime('%d.%m.%Y')} | {row[3]} € | {status}")


def handle_update_order(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for an order ID and updated amount, then update the order."""
    print("Enter Order ID to update:")
    try:
        order_id = int(input("Order ID: ").strip())
    except ValueError:
        print("Error: Order ID must be a number.")
        return

    order = get_order_by_id(order_id, connection)
    if not order:
        print("Validation Error: Order with ID does not exist.")
        return

    try:
        amount = Decimal(input("New Amount (€): ").strip())
    except Exception:
        print("Error: Amount must be a valid number.")
        return

    update_order(order_id, amount, connection)


def handle_cancel_order(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for an order ID and cancel it."""
    print("Enter Order ID to cancel:")
    try:
        order_id = int(input("Order ID: ").strip())
    except ValueError:
        print("Error: Order ID must be a number.")
        return

    order = get_order_by_id(order_id, connection)
    if not order:
        print("Validation Error: Order with ID does not exist.")
        return

    cancel_order(order_id, connection)


# ─── PRODUCT HANDLERS ─────────────────────────────────────────────────────────

def handle_create_product(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for product data and create a new product."""
    print("--- [ CREATE PRODUCT ] ---")
    name = input("Product Name: ").strip()
    unit = input("Unit (leave empty if none): ").strip() or None

    try:
        price = Decimal(input("Price (€): ").strip())
    except Exception:
        print("Error: Price must be a valid number.")
        return

    create_product(name, unit, price, connection)


def handle_get_products(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Display all products."""
    print("--- [ PRODUCTS ] ---")
    products = get_all_products(connection)

    if not products:
        print("No products found.")
        return

    for row in products:
        status = "ACTIVE" if row[4] else "INACTIVE"
        unit = row[2] if row[2] else "-"
        print(f"  #{row[0]} | {row[1]} | {unit} | {row[3]} € | {status}")


def handle_update_product(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for a product ID and updated data, then update the product."""
    print("Enter Product ID to update:")
    try:
        product_id = int(input("Product ID: ").strip())
    except ValueError:
        print("Error: Product ID must be a number.")
        return

    product = get_product_by_id(product_id, connection)
    if not product:
        print("Validation Error: Product with ID does not exist.")
        return

    print("--- [ UPDATE PRODUCT ] ---")
    name = input("Product Name: ").strip()
    unit = input("Unit (leave empty if none): ").strip() or None

    try:
        price = Decimal(input("Price (€): ").strip())
    except Exception:
        print("Error: Price must be a valid number.")
        return

    update_product(product_id, name, unit, price, connection)


def handle_deactivate_product(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """Prompt user for a product ID and deactivate it."""
    print("Enter Product ID to deactivate:")
    try:
        product_id = int(input("Product ID: ").strip())
    except ValueError:
        print("Error: Product ID must be a number.")
        return

    product = get_product_by_id(product_id, connection)
    if not product:
        print("Validation Error: Product with ID does not exist.")
        return

    deactivate_product(product_id, connection)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """
    Start the Notarnicola Data Management System.

    Displays an interactive main menu with submenus for GDPR,
    Customers, Orders and Products. Connects to the database
    once per session and closes the connection on exit.
    """
    connection = connect_2_db()

    if not connection:
        print("Connection Error: Could not connect to the database.")
        print("Please check if your db is running.")
        return

    while True:
        display_menu()
        user_input = input("Please select an option (1-5): ").strip()

        # ── GDPR ──
        if user_input == "1":
            while True:
                display_gdpr_menu()
                gdpr_choice = input("Please select an option (1-3): ").strip()

                if gdpr_choice == "1":
                    handle_access(connection)
                elif gdpr_choice == "2":
                    handle_anonymization(connection)
                elif gdpr_choice == "3":
                    break
                else:
                    print("Invalid Selection: Please type 1, 2, or 3.")

        # ── CUSTOMERS ──
        elif user_input == "2":
            while True:
                display_customer_menu()
                customer_choice = input("Please select an option (1-5): ").strip()

                if customer_choice == "1":
                    handle_create_customer(connection)
                elif customer_choice == "2":
                    handle_get_customer(connection)
                elif customer_choice == "3":
                    handle_update_customer(connection)
                elif customer_choice == "4":
                    handle_anonymization(connection)
                elif customer_choice == "5":
                    break
                else:
                    print("Invalid Selection: Please type 1 to 5.")

        # ── ORDERS ──
        elif user_input == "3":
            while True:
                display_order_menu()
                order_choice = input("Please select an option (1-5): ").strip()

                if order_choice == "1":
                    handle_create_order(connection)
                elif order_choice == "2":
                    handle_get_orders(connection)
                elif order_choice == "3":
                    handle_update_order(connection)
                elif order_choice == "4":
                    handle_cancel_order(connection)
                elif order_choice == "5":
                    break
                else:
                    print("Invalid Selection: Please type 1 to 5.")

        # ── PRODUCTS ──
        elif user_input == "4":
            while True:
                display_product_menu()
                product_choice = input("Please select an option (1-5): ").strip()

                if product_choice == "1":
                    handle_create_product(connection)
                elif product_choice == "2":
                    handle_get_products(connection)
                elif product_choice == "3":
                    handle_update_product(connection)
                elif product_choice == "4":
                    handle_deactivate_product(connection)
                elif product_choice == "5":
                    break
                else:
                    print("Invalid Selection: Please type 1 to 5.")

        # ── EXIT ──
        elif user_input == "5":
            print("Thank you for using Notarnicola Data Management. Goodbye!")
            break

        else:
            print("Invalid Selection: Please type 1 to 5.")

    close_db_connection(connection)


if __name__ == "__main__":
    main()