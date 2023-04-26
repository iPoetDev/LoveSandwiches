#!/user/bin/env python3
"""Module Run GSheet."""

# 0.1 Core Imports
import logging
import warnings

# 03. Local/Own Modules/Library
from data import DATASET, convert_data_from, get_sales_data, update_sales_worksheet
from settings import HOST, HTTPS, LOGS

# Logging
logging.basicConfig(filename=LOGS, level=logging.DEBUG)
logging.captureWarnings(True)
logging.info('Running on %s on port %d', HOST, HTTPS)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Database or exit program

print(DATASET)

data_list = get_sales_data()
sales_data = convert_data_from(data_list)
update_sales_worksheet(sales_data)

print(DATASET)
