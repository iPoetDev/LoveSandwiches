#!/user/bin/env python3
"""Module Connection Management."""

# 0.1 Core Imports
import sys

import projectlogging
from settings import LOGS

# 0.4 Log Cofiguration
projectlogging.configure_logging(LOGS)
LOGRS = projectlogging.configure_loguru()


def exiting_exception(error: Exception, message: str):
    """
    Make an exiting exception.
    1. Log the error
    2. Print the error
    3. Exit the program
    Parameters
    ----------
        :param error: Exception
        :type: Exception
        :param message: str
        :type: str
    Returns
    ----------
        :return: None
    """
    _error_context: str = f'{str(error).title}'
    _output: str = f'{_error_context}: {error}: {message}'
    LOGRS.error(_output)
    print(_output)
    sys.exit(1)


def input_correction(error: Exception, message: str, kind: str):
    """
    Gracefully allow a user to recover from a *NotFound exception.
    Parameters
    ----------
        :param error: Exception
        :type: Exception
        :param message: str
        :type: str
        :param kind: str: File or Tab
        :type: str
    Returns
    ----------
        :return: value_str - Returns a string for a file|tab name
        :rtype: str
    """
    # Log the error and print it
    _error_context: str = f'{str(error).title}'
    _output: str = f'{_error_context}: {error}: {message}'
    LOGRS.error(_output)
    # Status, Success and Prompt messages
    _status: str = f'{_output}'
    _success: str = f'User input:'
    _prompt: str = f"Enter the new {kind} name:"
    while True:
        print(_status)
        value_str = input(_prompt)
        LOGS.info(f"User input: {value_str}")
        print(value_str)
        if validate_input(value_str):
            print(_success, value_str, sep=" ")
            break
    
    return value_str


def creds_correction(credentials: str, file_type: str, message: str):
    """
        Gracefully allow a user to recover from a *NotFound exception.
        Parameters
        ----------
            :param error: Exception
            :type: Exception
            :param message: str
            :type: str
            :param kind: str: File or Tab
            :type: str
        Returns
        ----------
            :return: value_str - Returns a string for a file|tab name
            :rtype: str
        """
    # Log the error and print it
    _assert_context: str = f'Assert: Credentails File'
    _output: str = f'{_assert_context}: \n 2: {credentials} has a extension of .{file_type} \n 3: {message}'
    LOGRS.error(_output)
    # Status, Success and Prompt messages
    _status: str = f'{_output}'
    _success: str = f'User input:'
    _prompt: str = f"Enter the new {credentials} name with .json as extension:"
    while True:
        print(_status)
        value_str = input(_prompt)
        LOGS.info(f"User input: {value_str}")
        print(value_str)
        if validate_input(value_str):
            print(_success, value_str, sep=" ")
            break
    
    return value_str


def validate_input(value_str: str):
    """
    Validate the input.
    1: Asserting of string type
    2: Checking for length is 0
    
    Parameters
    ----------
        :param value_str: string input to validate
        :type: str
        
    Returns
    ----------
        :return: True if valid else False
        :rtype: bool
        
    Raises
    ----------
        :raises ValueError: if not string or length is 0
    """
    try:
        if not isinstance(value_str, str):
            raise ValueError("Incorrect Type. Must be string.")
        
        if len(value_str) == 0:
            raise ValueError("Incorrect Value.")
    except ValueError as error:
        print(f"{error}: Please enter a correct input to proceed.")
        return False
    
    return True
