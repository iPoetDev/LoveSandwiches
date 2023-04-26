#!/user/bin/env python3
"""Module Run GSheet."""

# 03. Local/Own Modules/Library
import connections
from settings import CRED_FILE, FILENAME, TAB_SALES

# Connections
# SSL_SOCK = open_connection()
CLIENT = connections.connect_to_remote(CRED_FILE)
DATASOURCE = connections.get_source(CLIENT, FILENAME)
SHEET = connections.open_sheet(DATASOURCE, TAB_SALES)
DATASET = connections.fetch_data(SHEET)


def new_sales_prompt(dataset):
    """
    Fetch, validate and prompt for new sales data,
    Then update remote sales data with new data,
    Finally refresh the local dataset.
    :param dataset: local dataset
    :type dataset: list[str]
    :return: sales_data
    :rtype: list[str]
    """
    print(dataset)
    data_list = get_sales_data()
    sales_data = convert_data_from(data_list)
    update_sales_worksheet(sales_data)
    refreshed_data = refresh_dataset()
    print(refreshed_data)
    return sales_data


def get_sales_data():
    """
    Get sales figures input from the user.
    :return: sales_data
    :rtype: list[str]
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
    :param values: data from user
    :type values: list[str]
    :param constraint: number of values required
    :type constraint: int
    :return: True if data is valid.
    :rtype: bool
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
    :param data: list of integers
    :type data: list[int]
    """
    _initiating: str = f"Updating {TAB_SALES.title()} worksheet...\n"
    _success: str = f"{TAB_SALES.title()} worksheet updated successfully.\n"
    print(_initiating)
    _worksheet = connections.open_sheet(DATASOURCE, TAB_SALES)
    _worksheet.append_row(data)
    print(_success)


def get_last_entries(count, tab):
    """
    Collects columns of data from a worksheet,
    collecting the last N entries for each record and
    returns the data as a list of lists.
    :param count: number of entries
    :type count: int
    :param tab: tab name
    :type tab: str
    :return: columns
    :rtype: list[list]
    """
    _init: int = 1
    _delimit: int = 1
    _number_of_rows = count
    _worksheet = connections.open_sheet(DATASOURCE, tab)
    
    _columns = []
    for ind in range(_init, _number_of_rows + _delimit):
        _column = _worksheet.col_values(ind)
        _columns.append(_column[-count:])
    return _columns


def convert_data_from(data: str):
    """
    Convert data from string to integer
    :param data: data from user
    :type data: str
    :return: data
    """
    return [int(num) for num in data]


def convert_data_to(data: list[int]):
    """
    Convert data from integer to string
    :param data: data from user
    :type data: list[int]
    :return: data
    :rtype: list[str]
    """
    return [str(num) for num in data]


def refresh_dataset():
    """
    Refresh sales dataset from Google Sheet
    """
    global DATASET
    DATASET = connections.fetch_data(SHEET)
    return DATASET
