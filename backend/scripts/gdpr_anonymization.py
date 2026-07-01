# gdpr_anonymization.py - GDPR Art. 17 right to erasure: anonymizes personal data of a customer
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


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