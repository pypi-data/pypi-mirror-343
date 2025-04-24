from functools import wraps
from inspect import signature, Parameter
from typing import Union, Literal, get_type_hints
from datetime import datetime, date, time
import os
import logging
 
user_home = os.path.expanduser("~")
log_dir = os.path.join(user_home, ".shadow-bot-assistant", "logs")
os.makedirs(log_dir, exist_ok=True)
 
logger = logging.getLogger(__name__)
log_file = os.path.join(log_dir, "sba.log")
logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)
 

def _log_errors(print_to_console=True, log_level=logging.ERROR):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if print_to_console:  
                    print(e)
                logger.log(log_level, f"Error in function '{func.__name__}': {e}", exc_info=True)  
                
        return wrapper
    return decorator


def _type_check_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        type_hints = get_type_hints(func)
        bind = sig.bind(*args, **kwargs)
        bind.apply_defaults()

        for name, value in bind.arguments.items():
            if name in type_hints:
                expected_type = type_hints[name]
                if not isinstance(value, expected_type):
                    raise TypeError(f"Argument '{name}' must be of type {expected_type}, got {type(value)} instead")

        return func(*args, **kwargs)
    return wrapper