#!/user/bin/env python3
"""Module Connection Management."""

# 0.1 Core Imports
import socket
import ssl

# 0.2 Core Modules
import gspread
from google.oauth2.service_account import Credentials

import exceptions
# 0.3 Project Logging
# 0.3 Local/Own Modules/Library
import projectlogging
from settings import DOMAINHOST, HTTPS, LOGS, SCOPE

# 0.4 Log Configuration
projectlogging.configure_logging(LOGS)
LOGRS = projectlogging.configure_loguru()

# 0.5 Exceptions: base GSpread Error
GSPREADERROR = gspread.exceptions.GSpreadException
# API Error
APIERROR = gspread.exceptions.APIError
# Trying to open non-existent or inaccessible worksheet. worksheet(title
WORKSHEETERROR = gspread.exceptions.WorksheetNotFound
# Trying to open non-existent or inaccessible spreadsheet.
# open(title, folder), open_by_url(url)
SPEADSHEETERROR = gspread.exceptions.SpreadsheetNotFound


# @Todo: set_timeout() https://docs.gspread.org/en/v5.7.2/api/client.html#gspread.Client.set_timeout
# @Todo: import_csv() https://docs.gspread.org/en/v5.7.2/api/client.html#gspread.Client.import_csv
# @Todo: create(title): https://docs.gspread.org/en/v5.7.2/api/client.html#gspread.Client.create
# @Todo: Client.session https://docs.gspread.org/en/v5.7.2/api/client.html#gspread.Client
# @Todo: Cell : https://docs.gspread.org/en/v5.7.2/api/models/cell.html#gspread.cell.Cell

def connect_to_remote(credential_file, file_type: str = "json"):
    """
    Synchronously connects to a Google Sheet using
    1: Cred.json file
    2: Scopes: Global
    
    Parameters
    ----------
        :param credential_file: str
        :type: str
        :param file_type: str
        :default: json
        :type: str
        
    Returns
    ----------
        A Scoped Credentialed Client
        :return: _creds.with_scopes(SCOPE)
        :rtype: gspread.client.Client
        
    Raises
    ----------
        Both exit the program
        :raises: NotImplementedError
        :raises: Exception
    """
    ftype = file_type.lower()
    _output: str = f'Credential file must be a json file: Given type: {ftype}'
    # if not isinstance(credential_file, str) or credential_file.endswith(f'.{ftype}'):
    #     credential_file = exceptions.creds_correction(credential_file, ftype, _output)
    
    # Authorise current client
    
    credentials: str = credential_file
    _creds = Credentials.from_service_account_file(credentials)
    # assert isinstance(_creds.with_scopes, SCOPE)
    try:
        if not _creds.requires_scopes:
            raise NotImplementedError
        
        # Authorise current client
        return _creds.with_scopes(SCOPE)
    
    except NotImplementedError as _notimplemented:
        _error_context: str = 'NotImplementedError'
        _notimplmessage: str = f'Credentials requires correct scopes. Check current {SCOPE}'
        _output: str = f'{_error_context}: {_notimplmessage}'
        exceptions.exiting_exception(_notimplemented, _output)


def get_source(credentials: Credentials, file_name: str):
    """
    Connects/opens to a Google Sheet synchronously else exit for now
    Parameters
    ----------
        :param credentials: Google sheet scoped credentials
        :type: google.auth.service_account.Credentials
        :param file_name: Google sheet file name
        :type: str
    Returns
    ----------
        :return: Spreadsheet
        :rtype: gspread.spreadsheet.Spreadsheet
    Raises
    ----------
        :raises: gspread.exceptions.SpreadsheetNotFound
    """
    # Authorise current client
    _gsheet = gspread.authorize(credentials)
    kind = "File"
    try:
        # Tests if existing sheet is the same aśa the configured filename
        if _gsheet.open(file_name).title != file_name:
            _titlechanged = f'{_gsheet.open(file_name).title} is not {file_name}'
            LOGRS.error(_titlechanged)
            raise SPEADSHEETERROR(_titlechanged)
        
        return _gsheet.open(file_name)
    except SPEADSHEETERROR as _notfound:
        _error_context: str = 'Spreadsheet Exception:'
        _request: str = f'Please enter correct file name: Previous: {file_name}'
        _instructions: str = 'Go to the google sheet and copy the file name'
        _output: str = f'1.{_error_context}: {str(_notfound)}\n 2.{_instructions}. \n3. {_request}.'
        # Gracefully handle this error by asking user to enter a correct file name
        newtitle = exceptions.input_correction(_notfound, _output, kind)
        return _gsheet.open(newtitle)


def open_sheet(file: gspread.Spreadsheet, tab: str):
    """
    Opens a given Google sheet's tab by tab name
    
    Parameters
    ----------
        :param file: Google sheet file
        :type: gspread.spreadsheet.Spreadsheet
        :param tab: Google sheet tab name
        :type:str
        
    Returns
    ----------
        :return: worksheet
        :rtype: gspread.worksheet.Worksheet
        
    Raises
    ----------
        Gracefully handle this error by asking user to enter a correct tab name
        :raises: gspread.exceptions.WorksheetNotFound
        :returns: worksheet
        :rtype: gspread.worksheet.Worksheet
    """
    kind = "Tab"
    try:
        return file.worksheet(tab)
    except WORKSHEETERROR as _notfound:
        _error_context: str = 'Worksheet Exception:'
        _request: str = f'Please enter correct {kind} name: Previous: {tab}'
        _instructions: str = f'Go to the google sheet and copy {kind} file name'
        _output: str = f'1.{_error_context}: {str(_notfound)}\n 2.{_instructions}. \n3. {_request}.'
        # Gracefully handle this error by asking user to enter a correct file name
        newtab = exceptions.input_correction(_notfound, _output, kind)
        return file.worksheet(newtab)


def fetch_data(sheet: gspread.Worksheet):
    """
    Fetch the data from the Google sheet
    
    Parameters
    ----------
        :param sheet:
        :type: gspread.worksheet.Worksheet
        
    Returns
    ----------
        :return: sheet.get_all_values()
        :rtype: list[str]
        
    Raises
    ----------
        Exits the program
        :raises: Exception
    """
    try:
        return sheet.get_all_values()
    except Exception as _error:
        _error_context: str = 'Exception'
        _output: str = f'{_error_context}: {_error}'
        exceptions.exiting_exception(_error, _output)


def open_ssl_connection():
    """
    Opens secure connects to outside network
    :return: _ssl
    :rtype: SSLSocket
    """
    _connection = ssl.create_default_context()
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _ssl = _connection.wrap_socket(_socket, server_hostname=DOMAINHOST)
    _ssl.connect((DOMAINHOST, HTTPS))
    return _ssl


def close_ssl_connection(sslsock: ssl.SSLSocket):
    """
    Closes secure connects to outside network
    :return:
    :rtype:
    """
    sslsock.close()
    sslsock = None
