# customers.py - CRUD operations for customers
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


# ─── CREATE ───────────────────────────────────────────────────────────────────

def create_customer(
    first_name: str,
    last_name: str,
    street: str,
    house_number: str,
    ort_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Insert a new customer into the database.

    Args:
        first_name (str): the customer's first name.
        last_name (str): the customer's last name.
        street (str): the customer's street name.
        house_number (str): the customer's house number.
        ort_id (int): the ID of the customer's location (FK to orte).
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the customer was created successfully, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO kunden (vorname, nachname, strasse, hausnummer, ort_id)
            VALUES (%s, %s, %s, %s, %s);
        """

        cursor.execute(query, (first_name, last_name, street, house_number, ort_id))
        connection.commit()

        print(f"Customer '{first_name} {last_name}' successfully created")
        return True

    except Error as e:
        connection.rollback()
        print(f"Create failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


# ─── READ ─────────────────────────────────────────────────────────────────────

def get_customer_master_data(
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
        print("Error: No active db connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT
                k.vorname AS FirstName,
                k.nachname AS LastName,
                k.strasse AS Street,
                k.hausnummer AS HouseNumber,
                o.plz AS PostalCode,
                o.stadt AS City
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
        print("Error: No active db connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT
                b.id AS OrderID,
                b.betrag AS Amount,
                b.bestelldatum AS Date
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
        print("Error: No active db connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT
                bp.id AS PositionID,
                bp.bestellung_id AS OrderID,
                bp.produkt_id AS ProductID,
                p.name AS ProductName,
                p.einheit AS Unit,
                p.preis AS Price,
                bp.menge AS Quantity
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


# ─── UPDATE ───────────────────────────────────────────────────────────────────

def update_customer(
    customer_id: int,
    first_name: str,
    last_name: str,
    street: str,
    house_number: str,
    ort_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Update an existing customer's personal data.

    Args:
        customer_id (int): the ID of the customer to update.
        first_name (str): the new first name.
        last_name (str): the new last name.
        street (str): the new street name.
        house_number (str): the new house number.
        ort_id (int): the new location ID (FK to orte).
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
            UPDATE kunden
            SET vorname = %s,
                nachname = %s,
                strasse = %s,
                hausnummer = %s,
                ort_id = %s
            WHERE id = %s;
        """

        cursor.execute(query, (first_name, last_name, street, house_number, ort_id, customer_id))
        connection.commit()

        print(f"Customer {customer_id} successfully updated")
        return True

    except Error as e:
        connection.rollback()
        print(f"Update failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


# ─── ANONYMIZE (GDPR Art. 17) ─────────────────────────────────────────────────

def anonymize_customer(
    customer_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Anonymize a customer's personal data by replacing their name with 'N/A'.

    Instead of physically deleting the customer, this function replaces
    the customer's first and last name with 'N/A' to comply with both
    GDPR Art. 17 (right to erasure) and §147 AO (10-year retention
    obligation for financial records). Order and billing data is
    preserved for legal and accounting purposes.

    Args:
        customer_id (int): the ID of the customer to anonymize.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the anonymization succeeded, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            UPDATE kunden
            SET vorname = 'N/A',
                nachname = 'N/A'
            WHERE id = %s;
        """

        cursor.execute(query, (customer_id,))
        connection.commit()

        print("Customer successfully anonymized")
        return True

    except Error as e:
        connection.rollback()
        print(f"Anonymization failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()