#!/user/bin/env python3
"""Module Run GSheet."""

# 0.1 Core Imports
import logging
import warnings

# 03. Local/Own Modules/Library
from data import DATASET, new_sales_prompt
from settings import HOST, HTTPS, LOGS, WELCOME
from stock import do_stock_take

# Logging
logging.basicConfig(filename=LOGS, level=logging.DEBUG)
logging.captureWarnings(True)
logging.info('Running on %s on port %d', HOST, HTTPS)
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Execute the main function as User Input entry point
def main():
    """ Main function to run the app."""
    new_sales = new_sales_prompt(DATASET)
    do_stock_take(new_sales, 1.1, 5)


print(WELCOME)
main()
