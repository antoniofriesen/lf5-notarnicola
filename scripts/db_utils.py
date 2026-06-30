# db_utils.py - shared database connection utilities
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

import os

import mysql.connector
from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from dotenv import load_dotenv


def connect_2_db() -> MySQLConnectionAbstract | PooledMySQLConnection | None:
    """
    Establish a connection to the MySQL database using credentials
    from the .env file.

    Returns:
        MySQLConnection | None: an active database connection if
        successful, otherwise None.
    """
    load_dotenv()

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
        )

        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection

    except Error as e:
        print(f"Connection to MySQL database error occurred: {e}")
        return None


def close_db_connection(connection: MySQLConnectionAbstract | PooledMySQLConnection | None) -> None:
    """
    Close an active MySQL database connection if one exists.

    Args:
        connection (MySQLConnection | None): the connection to close.
    """
    if connection is not None and connection.is_connected():
        connection.close()
        print("Successfully closed connection to MySQL database")