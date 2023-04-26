#!/user/bin/env python3
"""Module Run GSheet."""

# 03. Local/Own Modules/Library
import connections
from settings import FILENAME, TAB

# Connections
# SSL_SOCK = open_connection()
CLIENT = connections.connect_to_remote()
DATASOURCE = connections.get_source(CLIENT, FILENAME)
SHEET = connections.open_sheet(DATASOURCE, TAB)
DATASET = connections.fetch_data(SHEET)


# Connections
# closed_connection(SSL_SOCK)


def get_sales_data():
    """
    Get sales figures input from the user.
    """
    # Strings
    _request: str = "Please enter sales data from the last market."
    _instruction: str = "Data should be six numbers, separated by commas."
    _example: str = "10,20,30,40,50\n"
    _prompt: str = "Enter your data here: "
    _success: str = "Data is valid!"
    # Output
    while True:
        print(_request)
        print(_instruction)
        print(_example)
        # Input
        data_str = input(_prompt)
        print(f"The input provided: {data_str}. \n Was this correct?")
        sales_data = data_str.split(",")
        if validate_data(sales_data, 6):
            print(_success)
            break
    
    return sales_data


def validate_data(values, constraint):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there are not exactly 6 values.
    """
    _value_limit = constraint
    try:
        [int(value) for value in values]
        if len(values) != _value_limit:
            raise ValueError(
                    f"Exactly {_value_limit} values required, you provided {len(values)}"
                    )
    except ValueError as _error:
        print(f"Invalid data: {_error}, please try again.\n")
        return False
    
    return True


def update_sales_worksheet(data: list[int]):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    _initating: str = "Updating sales worksheet...\n"
    _success: str = "Sales worksheet updated successfully.\n"
    print(_initating)
    _worksheet = connections.open_sheet(DATASOURCE, TAB)
    _worksheet.append_row(data)
    print(_success)


def convert_data_from(data: str):
    """
    Convert data from string to integer
    :param data: data from user
    :type data: str
    :return: data
    """
    return [int(num) for num in data]
