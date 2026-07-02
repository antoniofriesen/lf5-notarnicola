# orders.py - CRUD operations for orders
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

from decimal import Decimal
from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


# ─── CREATE ───────────────────────────────────────────────────────────────────

def create_order(
    customer_id: int,
    amount: Decimal,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Insert a new order into the database.

    Args:
        customer_id (int): the ID of the customer placing the order.
        amount (Decimal): the total amount of the order.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the order was created successfully, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO bestellungen (kunden_id, betrag)
            VALUES (%s, %s);
        """

        cursor.execute(query, (customer_id, amount))
        connection.commit()

        print(f"Order for customer {customer_id} successfully created")
        return True

    except Error as e:
        connection.rollback()
        print(f"Create failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


# ─── READ ─────────────────────────────────────────────────────────────────────

def get_all_orders(
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> list:
    """
    Retrieve all orders from the database.

    Args:
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        list: a list of all orders, or an empty list if an error occurred.
    """
    if connection is None:
        print("Error: No active db connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT
                b.id AS OrderID,
                b.kunden_id AS CustomerID,
                b.bestelldatum AS Date,
                b.betrag AS Amount,
                b.storniert AS Cancelled
            FROM bestellungen b
            ORDER BY b.bestelldatum DESC;
        """

        cursor.execute(query)
        return cursor.fetchall()

    except Error as e:
        print(f"Query failed: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()


def get_order_by_id(
    order_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> list:
    """
    Retrieve a single order by its ID.

    Args:
        order_id (int): the ID of the order to look up.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        list: a list containing the order data, or an empty list if
        not found or an error occurred.
    """
    if connection is None:
        print("Error: No active db connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT
                b.id AS OrderID,
                b.kunden_id AS CustomerID,
                b.bestelldatum AS Date,
                b.betrag AS Amount,
                b.storniert AS Cancelled
            FROM bestellungen b
            WHERE b.id = %s;
        """

        cursor.execute(query, (order_id,))
        return cursor.fetchall()

    except Error as e:
        print(f"Query failed: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()


# ─── UPDATE ───────────────────────────────────────────────────────────────────

def update_order(
    order_id: int,
    amount: Decimal,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Update an existing order's amount.

    Args:
        order_id (int): the ID of the order to update.
        amount (Decimal): the new total amount.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            UPDATE bestellungen
            SET betrag = %s
            WHERE id = %s;
        """

        cursor.execute(query, (amount, order_id))
        connection.commit()

        print(f"Order {order_id} successfully updated")
        return True

    except Error as e:
        connection.rollback()
        print(f"Update failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


# ─── CANCEL ───────────────────────────────────────────────────────────────────

def cancel_order(
    order_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Mark an order as cancelled by setting the storniert flag to True.

    Instead of physically deleting the order, this function sets the
    storniert flag to preserve order history for accounting purposes.

    Args:
        order_id (int): the ID of the order to cancel.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the cancellation succeeded, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            UPDATE bestellungen
            SET storniert = TRUE
            WHERE id = %s;
        """

        cursor.execute(query, (order_id,))
        connection.commit()

        print(f"Order {order_id} successfully cancelled")
        return True

    except Error as e:
        connection.rollback()
        print(f"Cancellation failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()