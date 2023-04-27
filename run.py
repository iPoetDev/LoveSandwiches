#!/user/bin/env python3
"""Module Run GSheet."""
import sys

import loguru as logcatcher

import projectlogging
# 03. Local/Own Modules/Library
from data import DATASET, new_sales_prompt
from settings import LOGS, WELCOME
from stock import do_stock_take

projectlogging.configure_logging(LOGS)
projectlogging.configure_loguru()


# Execute the main function as User Input entry point
@logcatcher.catch(onerror=lambda _: sys.exit(1))
def main():
    """ Main function to run the app."""
    print(WELCOME)
    projectlogging.log_message(WELCOME)
    projectlogging.log_message(f"Starting...")
    new_sales = new_sales_prompt(DATASET)
    do_stock_take(new_sales, 1.1, 5)
    projectlogging.log_message(f"Done!")


print(WELCOME)

main()
