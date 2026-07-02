# locations.py - CRUD operations for locations
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


def get_or_create_location(
    plz: str,
    city: str,
    connection: MySQLConnectionAbstract | PooledMySQLConnection | None,
) -> int | None:
    """
    Look up a location by PLZ and city. If not found, create a new entry.

    Args:
        plz (str): the postal code of the location.
        city (str): the city name of the location.
        connection (MySQLConnectionAbstract | PooledMySQLConnection | None):
            an active database connection.

    Returns:
        int | None: the ort_id of the existing or newly created location,
        or None if an error occurred.
    """
    if connection is None:
        print("Error: No active db connection")
        return None

    cursor = None

    try:
        cursor = connection.cursor()

        # check if location already exists
        cursor.execute(
            "SELECT id FROM orte WHERE plz = %s AND stadt = %s;",
            (plz, city),
        )
        result = cursor.fetchone()

        if result:
            return result[0]

        # location not found — create new entry
        cursor.execute(
            "INSERT INTO orte (plz, stadt) VALUES (%s, %s);",
            (plz, city),
        )
        connection.commit()
        return cursor.lastrowid

    except Error as e:
        connection.rollback()
        print(f"Location lookup/create failed: {e}")
        return None

    finally:
        if cursor is not None:
            cursor.close()