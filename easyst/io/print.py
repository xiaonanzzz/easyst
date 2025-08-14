import streamlit as st
import pandas as pd
import builtins
from contextlib import contextmanager


@contextmanager
def custom_print(redirect_func):
    """
    Custom print function that redirects output to a specified function.
    Usage example:
    ```python
    # Redirect print to Streamlit
    with custom_print(st_print):
        print("Hello, world!")
    ```
    Args:
        redirect_func: The function to redirect output to.
    """
    original_print = builtins.print

    def new_print(*args, **kwargs):
        redirect_func(*args, **kwargs)

    builtins.print = new_print
    try:
        yield
    finally:
        builtins.print = original_print

def st_print(*args, **kwargs):
    """
    Print to Streamlit
    """
    for arg in args:
        if isinstance(arg, str):
            st.write(arg)
        elif isinstance(arg, pd.DataFrame):
            st.dataframe(arg)
        elif isinstance(arg, (dict, list)):
            st.json(arg)
        else:
            st.write(arg)