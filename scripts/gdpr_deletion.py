# gdpr_deletion.py - GDPR Art. 17 right to erasure: deletes all stored data of a customer
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


def delete_order_positions(
    customer_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Delete all order positions associated with a customer's orders.

    Must be called before delete_orders(), since order positions
    reference orders via a foreign key.

    Args:
        customer_id (int): the ID of the customer whose order
            positions should be deleted.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the deletion succeeded, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            DELETE bp
            FROM bestellpositionen bp
            INNER JOIN bestellungen b ON b.id = bp.bestellung_id
            INNER JOIN kunden k ON k.id = b.kunden_id
            WHERE k.id = %s;
        """

        cursor.execute(query, (customer_id,))
        connection.commit()

        print("Order positions successfully deleted")
        return True

    except Error as e:
        connection.rollback()
        print(f"Delete failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


def delete_orders(
    customer_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Delete all orders belonging to a customer.

    Must be called after delete_order_positions() and before
    delete_customer(), since orders reference customers via a
    foreign key.

    Args:
        customer_id (int): the ID of the customer whose orders
            should be deleted.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the deletion succeeded, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            DELETE b
            FROM bestellungen b
            INNER JOIN kunden k ON k.id = b.kunden_id
            WHERE k.id = %s;
        """

        cursor.execute(query, (customer_id,))
        connection.commit()

        print("Orders successfully deleted")
        return True

    except Error as e:
        connection.rollback()
        print(f"Delete failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


def delete_customer(
    customer_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Delete a customer's master data.

    Must be called last, after delete_order_positions() and
    delete_orders(), since other tables reference this customer
    via foreign keys.

    Args:
        customer_id (int): the ID of the customer to delete.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the deletion succeeded, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            DELETE
            FROM kunden
            WHERE id = %s;
        """

        cursor.execute(query, (customer_id,))
        connection.commit()

        print("Customer successfully deleted")
        return True

    except Error as e:
        connection.rollback()
        print(f"Delete failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()