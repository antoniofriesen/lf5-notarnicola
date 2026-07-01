# main.py - Central entry point for GDPR Access and Deletion Management
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

import gdpr_access
import gdpr_deletion
from db_utils import connect_2_db, close_db_connection
from helpers import display_menu, get_valid_customer_id
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


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
    master_data = gdpr_access.get_all_customer_master_data(customer_id, connection)

    if not master_data:
        print("Validation Error: Customer with ID does not exist.")
        return

    orders = gdpr_access.get_customer_orders(customer_id, connection)
    positions = gdpr_access.get_customer_order_positions(customer_id, connection)

    print("--- [ CUSTOMER MASTER DATA ] ---")
    print(master_data)

    print("--- [ CUSTOMER ORDERS ] ---")
    print(orders)

    print("--- [ CUSTOMER ORDER POSITIONS ] ---")
    print(positions)


def handle_deletion(
    connection: MySQLConnectionAbstract | PooledMySQLConnection,
) -> None:
    """
    Handle a GDPR Art. 17 erasure request.

    Prompts the user for a customer ID, verifies the customer exists,
    asks for confirmation, then cascades deletion of all related data
    in the correct order to respect foreign key constraints.

    Args:
        connection (MySQLConnectionAbstract | PooledMySQLConnection):
            an active database connection.
    """
    print("Enter Customer ID to be deleted:")
    customer_id = get_valid_customer_id()

    print("Searching for Customer ID...")
    master_data = gdpr_access.get_all_customer_master_data(customer_id, connection)

    if not master_data:
        print("Validation Error: Deletion impossible. Customer ID does not exist.")
        return

    print("WARNING: You are about to permanently delete this customer!")

    while True:
        print("Are you absolutely sure? (yes/no):")
        confirmation = input().strip().lower()

        if confirmation in ["yes", "y", "ja", "j"]:
            step1_success = gdpr_deletion.delete_order_positions(customer_id, connection)
            if not step1_success:
                print("Error: Could not delete order positions. Deletion aborted.")
                return

            step2_success = gdpr_deletion.delete_orders(customer_id, connection)
            if not step2_success:
                print("Error: Could not delete orders. Deletion aborted.")
                return

            step3_success = gdpr_deletion.delete_customer(customer_id, connection)
            if not step3_success:
                print("Error: Could not delete customer. Deletion aborted.")
                return

            print("Success: Customer and all related data deleted.")
            return

        elif confirmation in ["no", "n", "nein"]:
            print("Deletion canceled by user.")
            return

        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def main() -> None:
    """
    Start the GDPR Data Management System.

    Displays an interactive menu in a loop, connecting to the database
    only when needed and closing the connection after each operation.
    """
    while True:
        display_menu()
        user_input = input("Please select an option (1-3): ").strip()

        if user_input in ["1", "2"]:
            connection = connect_2_db()

            if not connection:
                print("Connection Error: Could not connect to the database.")
                print("Please check if your db is running.")
                continue

            if user_input == "1":
                handle_access(connection)
            elif user_input == "2":
                handle_deletion(connection)

            close_db_connection(connection)

        elif user_input == "3":
            print("Thank you for using GDPR Data Management. Goodbye!")
            break

        else:
            print("Invalid Selection: Please type 1, 2, or 3.")


if __name__ == "__main__":
    main()