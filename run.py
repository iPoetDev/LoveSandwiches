#!/user/bin/env python3
"""Module Run GSheet."""

# @0min53
# 0.1 Core Imports
import logging
import os
import socket
import ssl
import sys
# 0.2 Core Modules
from pathlib import Path

# 0.3 Dedicated Modules/Imports
from notion.client import NotionClient

# String/Int Resources
HOST: str = 'www.notion.so'
HTTPS: int = 443
LOGS: str = 'notion-py.log'
ENV: str = '.env'
KEY: str = 'NOTION_KEY'
DB_ID: str = 'NOTION_DATABASE_ID'

# Logging
logging.basicConfig(filename=LOGS, level=logging.DEBUG)
# Notion: Load .env file SECRETS or throw a ModuleNotFoundError
# ADR XXX: Use dotenv to load .env file to develop with env vars early. URI: https://pypi.org/project/python-dotenv/
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    not_found: str = 'ModuleNotFoundError: dotenv'
    output_message: str = f'Could not load {ENV} file. Import python-dotenv to load external {ENV} '
    logging.error(f'{not_found}: {output_message}')
    print(f'{not_found}: {output_message}')
else:
    dotenv_path = Path(ENV)
    load_dotenv(dotenv_path=dotenv_path)

# Notion: Load env vars
NOTION_KEY = os.getenv(KEY)
NOTION_DATABASE_ID = os.getenv(DB_ID)
key_message: str = f'{KEY} is empty. Please set {KEY} in {ENV} file.'
db_message: str = f'{DB_ID} is empty. Please set {DB_ID} in {ENV} file.'
# Checks & Exits
while NOTION_KEY == '' or NOTION_KEY is None:
    print(key_message)
    sys.exit(1)

while NOTION_KEY == '' or NOTION_KEY is None:
    print(db_message)
    sys.exit(1)


def connect_to_notion_client() -> NotionClient:
    """
    Connects to a Notion database synchronously else exit for now
    :return: collection
    :rtype: NotionClient
    """
    try:
        # Initialize a new Notion client
        client = NotionClient(token_v2=NOTION_KEY)
        # Get the specified database
        collection: NotionClient = client.get_collection_view(NOTION_DATABASE_ID)
        # Return database
        return collection
    except Exception as error:
        logging.error(f'Exception: {error}')
        print(f'Exception: {error}. Check the logs for more details.')
        sys.exit(1)


def open_connection():
    """
    Opens secure connects to outside network
    :return:
    :rtype:
    """
    connection = ssl.create_default_context()
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _ssl = connection.wrap_socket(_socket, server_hostname=HOST)
    _ssl.connect((HOST, HTTPS))
    return _ssl


def closed_connection(_ssl: ssl.SSLSocket):
    """
    Closes secure connects to outside network
    :return:
    :rtype:
    """
    _ssl.close()
    _ssl = None


# Connections
# SSL_SOCK = open_connection()
# Database or exit program
client = connect_to_notion_client()
# Connections
# closed_connection(SSL_SOCK)
