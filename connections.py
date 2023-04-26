#!/user/bin/env python3
"""Module Connection Management."""

# 0.1 Core Imports
import logging
import socket
import ssl
import sys

# 0.2 Core Modules
import gspread
from google.oauth2.service_account import Credentials

# 0.3 Local/Own Modules/Library
from settings import DOMAINHOST, HOST, HTTPS, LOGS, SCOPE

# Logging
logging.basicConfig(filename=LOGS, level=logging.DEBUG)
logging.captureWarnings(True)
logging.info('Running on %s on port %d', HOST, HTTPS)


def connect_to_remote(credential_file):
    """
    Connects to a Google Sheet synchronously else exit for now
    :return: collection
    :rtype: NotionClient
    """
    try:
        _creds = Credentials.from_service_account_file(credential_file)
        # assert isinstance(_creds.with_scopes, SCOPE)
        return _creds.with_scopes(SCOPE)
    except Exception as _error:
        _error_context: str = 'Exception'
        _output: str = f'{_error_context}: {_error}'
        logging.error(_output)
        print(_output)
        sys.exit(1)


def get_source(credentials, file_name: str):
    """
    Connects to a Google Sheet synchronously else exit for now
    :param credentials: Google sheet credentials
    :type credentials: Credentials
    :param file_name: Google sheet file name
    :type file_name: str
    :return: GSpreadClient
    :rtype:
    """
    try:
        _gsheet_client = gspread.authorize(credentials)
        return _gsheet_client.open(file_name)
    except Exception as _error:
        _error_context: str = 'Exception'
        _output: str = f'{_error_context}: {_error}'
        logging.error(_output)
        print(_output)
        sys.exit(1)


def open_sheet(file: gspread.Spreadsheet, tab: str):
    """
    Opens a Google sheet by tabname
    :param file: Google sheet file
    :type file: GSpreadClient
    :param tab: Google sheet tab
    :type tab: str
    :return: worksheet
    :rtype:
    """
    try:
        return file.worksheet(tab)
    except Exception as _error:
        _error_context: str = 'Exception'
        _output: str = f'{_error_context}: {_error}'
        logging.error(_output)
        print(_output)
        sys.exit(1)


def fetch_data(sheet: gspread.Worksheet):
    """
    Fetch the data from the Google sheet
    :param sheet:
    :type sheet:
    :return: sheet.get_all_values()
    :rtype: list[str]
    """
    try:
        return sheet.get_all_values()
    except Exception as _error:
        _error_context: str = 'Exception'
        _output: str = f'{_error_context}: {_error}'
        logging.error(_output)
        print(_output)
        sys.exit(1)


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
