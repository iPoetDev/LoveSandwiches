#!/user/bin/env python3
"""Module App Settings and Environmental Vars."""

# @0min53
# 0.1 Core Imports
import logging
# 0.2 Core Modules
from pathlib import Path

# Global String/Int Resources
DOMAINHOST: str = 'www.google.com'
HOST: str = 'www.googleapis.com'
APIHOST: str = 'www.googleapis.com'
CRED_FILE: str = 'creds.json'
HTTPS: int = 443
LOGS: str = 'goggle-py.log'
ENV: str = '.env'
ENCODE: str = 'UTF-8'
WARNACTION: str = 'ignore'

WELCOME: str = 'Welcome to Love Sandwiches Data Automation'

# Data String/Int Resources
FILENAME: str = 'LoveSandwiches'
TAB_SALES: str = 'sales'
TAB_STOCK: str = 'stock'
TAB_SURPLUS: str = 'surplus'

# Logging
logging.basicConfig(filename=LOGS, level=logging.DEBUG)
logging.captureWarnings(True)
logging.info('Running on %s on port %d', HOST, HTTPS)

SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
        ]


def load_env():
    """
    Load .env file to develop with env vars early.
    """
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError as notfound_error:
        error_context: str = 'ModuleNotFoundError: dotenv'
        issue_message: str = f'Could not load {ENV} file.'
        guidance_message: str = f'Import python-dotenv to load external {ENV} or check the ENV file path. '
        output: str = f'{error_context}: {issue_message} - {guidance_message}'
        logging.error(output)
        print(output)
        logging.debug('Module: %s: as %r', str(notfound_error), notfound_error, exc_info=True)
    else:
        # With statement / Context management to load .env file and handle closure of path/files
        success_message: str = f'Successfully loaded {ENV} file.'
        # Get the path of the .env file
        dotenv_path: Path = Path(ENV)
        # Open the .env file and then load/close the .env file if a file exists
        with dotenv_path.open(encoding=ENCODE) as dotenv_file:
            load_dotenv(dotenv_path=dotenv_path)
            logging.debug(success_message)
        print(success_message)
