#!/user/bin/env python3
"""Module Run GSheet."""

# 03. Local/Own Modules/Library
import connections
from data import DATASOURCE, convert_data_to, get_last_entries
from settings import TAB_STOCK, TAB_SURPLUS

STOCKSHEET = connections.open_sheet(DATASOURCE, TAB_STOCK)
STOCKDATA = connections.fetch_data(STOCKSHEET)
SURPLUSSHEET = connections.open_sheet(DATASOURCE, TAB_SURPLUS)
SURPLUSDATA = connections.fetch_data(STOCKSHEET)


def do_stock_take(sales_data: list[str], factor: float, transaction_total: int = 5):
    """
    Run the stock take.
    Updates the surplus and stock worksheet.
    Refreshes the local datasets
    :param sales_data: Sales data
    :type sales_data: list[str]
    :param transaction_total: number of transactions for the day
    :type transaction_total: int
    :param factor: factor to increase/decrease stock by a percentage
    :type factor: float
    """
    # 1: Manage Surplus
    _surplus = calculate_surplus(sales_data)
    update_surplus(_surplus)
    refesh_surplus()
    # 2: Stick Take
    _update_cols = get_last_entries(transaction_total, TAB_STOCK)
    _stock = calculate_stock(_update_cols, factor)
    update_stock(_stock)
    refesh_stock()


# ############################################STOCK###############################################
def calculate_stock(stocklist: list[list], factor: float = 1):
    """
    Calculate the stock for each item type.
    Add a factor increase/decrease to the stock.
    :param stocklist: Sales data
    :type stocklist: list[str]
    :param factor: factor to increase/decrease stock by a percentage
    :default factor: 1
    :type factor: float
    :return: Stock_data
    :rtype: list[int]
    """
    _initialiser: str = "Calculating stock data...\n"
    print(_initialiser)
    
    stock_data = []
    for column in stocklist:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * factor
        stock_data.append(round(stock_num))
    
    return stock_data


def update_stock(data):
    """
    Update stock worksheet, add new row with the list data provided.
    Prints user messages to the console.
    :param data: Stock data
    :type data: list[int]
    """
    _initialiser: str = f"Updating {TAB_STOCK.title()} worksheet...\n"
    _success: str = f"{TAB_STOCK.title()} worksheet updated successfully.\n"
    print(_initialiser)
    surplus_worksheet = connections.open_sheet(DATASOURCE, TAB_STOCK)
    surplus_worksheet.append_row(convert_data_to(data))
    refesh_stock()
    print(_success)


def refesh_stock():
    """
    Refresh local global stock dataset from Google Sheet
    :return: STOCKDATA
    :rtype: list[str]
    """
    global STOCKDATA
    STOCKDATA = connections.fetch_data(STOCKSHEET)
    return STOCKDATA


# ############################################SURPLUS###############################################
def calculate_surplus(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    :param sales_row: Sales data
    :type sales_row: list[str]
    :return: Surplus_data
    :rtype: list[int]
    """
    _initialiser: str = "Calculating surplus data...\n"
    print(_initialiser)
    stock_sheet = connections.open_sheet(DATASOURCE, TAB_STOCK)
    stock = connections.fetch_data(stock_sheet)
    stock_row = stock[-1]
    # Return the list comprehension as surplus data
    return [int(stock) - sales for stock, sales in zip(stock_row, sales_row)]


def update_surplus(data):
    """
    Update sales worksheet, add new row with the list data provided.
    Prints user messages to the console.
    :param data: Surplus data
    :type data: list[int]
    """
    _initialiser: str = f"Updating {TAB_SURPLUS.title()} worksheet...\n"
    _success: str = f"{TAB_SURPLUS.title()} worksheet updated successfully.\n"
    print(_initialiser)
    surplus_worksheet = connections.open_sheet(DATASOURCE, TAB_SURPLUS)
    surplus_worksheet.append_row(convert_data_to(data))
    refesh_surplus()
    print(_success)


def refesh_surplus():
    """
    Refresh local surplus dataset from Google Sheet
    :return: SURPLUSDATA
    :rtype: list[str]
    """
    global SURPLUSDATA
    SURPLUSDATA = connections.fetch_data(SURPLUSSHEET)
    return SURPLUSDATA
