# gdpr_access.py - GDPR Art. 15 right of access: outputs all stored data of a customer
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


def get_all_customer_master_data(
    customer_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> list:
    """
    Retrieve the master data (name and address) of a single customer.

    Args:
        customer_id (int): the ID of the customer to look up.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        list: a list containing the customer's master data, or an
        empty list if the customer was not found or an error occurred.
    """
    if connection is None:
        print("Error connecting to DB: No active connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT
                k.vorname AS Vorname,
                k.nachname AS Nachname,
                k.strasse AS Straße,
                k.hausnummer AS Hausnummer,
                o.plz AS PLZ,
                o.stadt AS Stadt
            FROM kunden k
            JOIN orte o ON o.id = k.ort_id
            WHERE k.id = %s;
        """

        cursor.execute(query, (customer_id,))
        return cursor.fetchall()

    except Error as e:
        print(f"Query failed: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()


def get_customer_orders(
    customer_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> list:
    """
    Retrieve all orders placed by a single customer.

    Args:
        customer_id (int): the ID of the customer to look up.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        list: a list of the customer's orders, or an empty list if
        none were found or an error occurred.
    """
    if connection is None:
        print("Error connecting to DB: No active connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT
                b.id AS BestellungsID,
                b.betrag AS Betrag,
                b.bestelldatum AS Datum
            FROM bestellungen b
            JOIN kunden k ON k.id = b.kunden_id
            WHERE k.id = %s;
        """

        cursor.execute(query, (customer_id,))
        return cursor.fetchall()

    except Error as e:
        print(f"Query failed: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()


def get_customer_order_positions(
    customer_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> list:
    """
    Retrieve all order positions (products and quantities) belonging
    to a single customer's orders.

    Args:
        customer_id (int): the ID of the customer to look up.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        list: a list of the customer's order positions, or an empty
        list if none were found or an error occurred.
    """
    if connection is None:
        print("Error connecting to DB: No active connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT
                bp.id AS PositionsID,
                bp.bestellung_id AS BestellungsID,
                bp.produkt_id AS ProduktID,
                p.name AS ProduktName,
                p.einheit AS Einheit,
                p.preis AS Preis,
                bp.menge AS Menge
            FROM bestellpositionen bp
            INNER JOIN produkte p ON p.id = bp.produkt_id
            INNER JOIN bestellungen b ON b.id = bp.bestellung_id
            INNER JOIN kunden k ON k.id = b.kunden_id
            WHERE k.id = %s;
        """

        cursor.execute(query, (customer_id,))
        return cursor.fetchall()

    except Error as e:
        print(f"Query failed: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()