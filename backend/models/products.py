# products.py - CRUD operations for products
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer


# IMPORTS
from decimal import Decimal
from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

# ─── CREATE ───────────────────────────────────────────────────────────────────

def create_product(
    name: str,
    unit: str | None,
    price: Decimal,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Insert a new product into the database.

    Args:
        name (str): name of the new product.
        unit (str | None): if a unit is available, this is the unit the product belongs to.
        price (Decimal): price of the product.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the product was created successfully, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO produkte (name, einheit, preis, aktiv)
            VALUES (%s, %s, %s, TRUE);
        """

        cursor.execute(query, (name, unit, price))
        connection.commit()

        print(f"Product successfully created")
        return True

    except Error as e:
        connection.rollback()
        print(f"Create failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


# ─── READ ─────────────────────────────────────────────────────────────────────

def get_all_products(
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> list:
    """
    Retrieve all products from the database.

    Args:
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        list: a list of all products, or an empty list if an error occurred.
    """
    if connection is None:
        print("Error: No active db connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT id, name, einheit, preis, aktiv
            FROM produkte
            ORDER BY name;
        """

        cursor.execute(query)
        return cursor.fetchall()

    except Error as e:
        print(f"Query failed: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()


def get_product_by_id(
    product_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> list:
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): the ID of the product to look up.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        list: a list containing the product data, or an empty list if
        not found or an error occurred.
    """
    if connection is None:
        print("Error: No active db connection")
        return []

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            SELECT id, name, einheit, preis, aktiv
            FROM produkte
            WHERE id = %s;
        """

        cursor.execute(query, (product_id,))
        return cursor.fetchall()

    except Error as e:
        print(f"Query failed: {e}")
        return []

    finally:
        if cursor is not None:
            cursor.close()


# ─── UPDATE ───────────────────────────────────────────────────────────────────

def update_product(
    product_id: int,
    name: str,
    unit: str | None,
    price: Decimal,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Update an existing product.

    Args:
        product_id (int): the ID of the order to update.
        name (str): the name of the product.
        unit (str): the unit the product belongs to.
        price (Decimal): the new price of the product.
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
            UPDATE produkte
            SET name = %s,
                einheit = %s,
                preis = %s
            WHERE id = %s;
        """

        cursor.execute(query, (name, unit, price, product_id))
        connection.commit()

        print(f"Product {product_id} successfully updated")
        return True

    except Error as e:
        connection.rollback()
        print(f"Update failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()


# ─── DEACTIVATE ───────────────────────────────────────────────────────────────────

def deactivate_product(
    product_id: int,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> bool:
    """
    Mark a product as inactive by setting the active flag to False.

    Instead of physically deleting the product, this function unsets the
    active flag to preserve product data.

    Args:
        product_id (int): the ID of the product to unset active flag.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        bool: True if the unset action succeeded, False otherwise.
    """
    if connection is None:
        print("Error: No active db connection")
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        query = """
            UPDATE produkte
            SET aktiv = FALSE
            WHERE id = %s;
        """

        cursor.execute(query, (product_id,))
        connection.commit()

        print(f"Product {product_id} successfully set as inactive ")
        return True

    except Error as e:
        connection.rollback()
        print(f"Cancellation failed: {e}")
        return False

    finally:
        if cursor is not None:
            cursor.close()