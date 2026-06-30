# dsgvo_auskunft.py - DSGVO Art. 15 right of access: outputs all stored data of a customer
# Author: Antonio Friesen, Julian Brandtstaedter, Thore Heuer

# IMPORTS
# connect_2_db from db_utils.py
# close_db_connection from db_utils.py

# function get_all_customer_master_data(id, connection)
#   if connection is null then
#       print message like "Error: No active db connection"
#       return empty_list
#   end if
#
#   try
#       create query using database_cursor
#       define query = here comes the query
#
#       execute query using database_cursor
#       fetch all_rows from database_cursor as costumer_master_data
#
#       return costumer_data
#
#   catch database_error as error
#       print message like "Query failed: " + error.message
#       return empty_list
#
#   finally
#       close database_cursor
#   end try
# end function

# function get_customer_orders(id, connection)
#   if connection is null then
#       print message like "Error: No active db connection"
#       return empty_list
#   end if
#
#   try
#       create query using database_cursor
#       define query = here comes the query
#
#       execute query using database_cursor
#       fetch all_rows from database_cursor as costumer_orders
#
#       return costumer_orders
#
#   catch database_error as error
#       print message like "Query failed: " + error.message
#       return empty_list
#
#   finally
#       close database_cursor
#   end try
# end function

# function get_customer_order_positions(id, connection)
#   if connection is null then
#       print message like "Error: No active db connection"
#       return empty_list
#   end if
#
#   try
#       create query using database_cursor
#       define query = here comes the query
#
#       execute query using database_cursor
#       fetch all_rows from database_cursor as costumer_order_positions
#
#       return costumer_order_positions
#
#   catch database_error as error
#       print message like "Query failed: " + error.message
#       return empty_list
#
#   finally
#       close database_cursor
#   end try
# end function

def main() -> None:
    """Main function"""
# connection = connect_2_db()
# customer_master_data = get_all_customer_master_data(id, connection)
# orders = get_customer_orders(id, connection)
# order_positions = get_customer_order_positions(id, connection)
# close_db_connection(connection)

if __name__ == "__main__":
    main()