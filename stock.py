#!/user/bin/env python3
"""Module Run GSheet."""

# 03. Local/Own Modules/Library
import connections
from data import DATASOURCE, convert_data_to, get_last_entries
from settings import TAB_STOCK, TAB_SURPLUS

# 0.4 Global Connections and Datasets: Primary
STOCKSHEET = connections.open_sheet(DATASOURCE, TAB_STOCK)
STOCKDATA = connections.fetch_data(STOCKSHEET)
SURPLUSSHEET = connections.open_sheet(DATASOURCE, TAB_SURPLUS)
SURPLUSDATA = connections.fetch_data(STOCKSHEET)


def do_stock_take(sales_data: list[str], factor: float, transaction_total: int = 5):
    """
    Run the stock take.
    Updates the surplus and stock worksheet.
    Refreshes the local datasets
    
    Parameters:
    ---------
        :param: sales_data: Sales data
        :type: sales_data: list[str]
        :param transaction_total: number of transactions for the day
        :type: transaction_total: int
        :default: transaction_total: 5
        :param: factor: factor to increase/decrease stock by a percentage
        :type: factor: float
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
def calculate_stock(stocklist: list[list], factor: float = 1.0):
    """
    Calculate the stock for each item type.
    Add a factor increase/decrease to the stock.
    
    Parameters:
    ---------
        :param stocklist: Sales data
        :type stocklist: list[str]
        :param factor: factor to increase/decrease stock by a percentage
        :default factor: 1.0
        :type factor: float
        :return: Stock_data
        :rtype: list[int]
    """
    _initialiser: str = "Calculating stock data...\n"
    print(_initialiser)
    
    stock_data = []
    zero_stock = 0.0
    for column in stocklist:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column) if int_column else zero_stock
        stock_num = average * factor
        stock_data.append(round(stock_num))
    
    return stock_data


def update_stock(data):
    """
    Update stock worksheet, add new row with the list data provided.
    Prints user messages to the console.
    
    Parameters:
    ---------
        :param data: Stock data
        :type data: list[int]
    """
    _initialiser: str = f"Updating {TAB_STOCK.title()} worksheet...\n"
    _success: str = f"{TAB_STOCK.title()} worksheet updated successfully.\n"
    print(_initialiser)
    surplus_worksheet = connections.open_sheet(DATASOURCE, TAB_STOCK)
    # Convert data list[int] to list[str]; before appending to worksheet
    surplus_worksheet.append_row(convert_data_to(data))
    refesh_stock()
    print(_success)


def refesh_stock():
    """
    Refresh local global stock dataset from Google Sheet.
    
    Parameters:
    ---------
        :identifier: global
        :return: STOCKDATA: global
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
    
    Parameters:
    ---------
        :param: sales_row - Sales data
        :type: list[str]
        :return: surplus_data: Surplus data
        :rtype: list[int]
    """
    _initialiser: str = "Calculating surplus data...\n"
    shift_index: int = 1
    start_index: int = 1
    default_val = "0"
    try:
        print(_initialiser)
        stock_sheet = connections.open_sheet(DATASOURCE, TAB_STOCK)
        stock = connections.fetch_data(stock_sheet)
        if stock_sheet.row_count == 0:
            stock_sheet.insert_row([default_val] * len(sales_row), start_index)
            stock_row = [default_val] * len(sales_row)
        else:
            # To access the last item on the list, use -1
            stock_row = stock * (len(stock) - shift_index)
    except connections.APIERROR as error:
        index_out_of_range = "list index out of range"
        print(error)
        # Handle Out of Range error by creating the first row of the worksheet with default values
        if index_out_of_range in str(error):
            # Reconnect to the stock sheet after APIERROR is raised.
            stock_sheet = connections.open_sheet(DATASOURCE, TAB_STOCK)
            if stock_sheet.row_count == 0:
                # Insert a new row at the start of the stock sheet.
                stock_sheet.insert_row([default_val] * len(sales_row), start_index)
                # Fetch the new stock data.
                stock_row = [default_val] * len(sales_row)
            else:
                raise error
        else:
            raise error
    # Return the list comprehension as surplus data
    return [int(stock) - sales for stock, sales in zip(stock_row, sales_row)]


def update_surplus(data: list[int]):
    """
    Update sales worksheet, add new row with the list data provided.
    Prints user messages to the console.
    
    Parameters:
    ---------
        :param: data: Surplus data
        :type: list[int]
    """
    _initialiser: str = f"Updating {TAB_SURPLUS.title()} worksheet...\n"
    _success: str = f"{TAB_SURPLUS.title()} worksheet updated successfully.\n"
    print(_initialiser)
    surplus_worksheet = connections.open_sheet(DATASOURCE, TAB_SURPLUS)
    # Convert data list[int] to list[str]; before appending to worksheet
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
