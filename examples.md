# easyst Examples

This file contains examples for the functions in the `easyst.io.print` module.

## Functions Overview

The `easyst.io.print` module provides utilities for redirecting Python's built-in `print` function and formatting output for Streamlit applications.

## 1. `custom_print` Function

The `custom_print` function is a context manager that temporarily redirects Python's built-in `print` function to a custom function.

### Basic Usage

```python
import streamlit as st
from easyst.io.print import custom_print, st_print

# Redirect print to Streamlit
with custom_print(st_print):
    print("Hello, World!")
    print("This will be displayed in Streamlit")
    print("Numbers:", 42, 3.14)
```

### Redirecting to Custom Functions

```python
import streamlit as st
from easyst.io.print import custom_print

def log_to_file(*args, **kwargs):
    """Custom function to log output to a file"""
    with open("output.log", "a") as f:
        for arg in args:
            f.write(str(arg) + " ")
        f.write("\n")

# Redirect print to file logging
with custom_print(log_to_file):
    print("This will be logged to output.log")
    print("Multiple arguments:", "arg1", "arg2", 123)
```

### Nested Context Managers

```python
import streamlit as st
from easyst.io.print import custom_print, st_print

def debug_print(*args, **kwargs):
    """Debug print function"""
    print(f"[DEBUG] {' '.join(map(str, args))}")

# You can nest context managers
with custom_print(st_print):
    print("This goes to Streamlit")
    
    with custom_print(debug_print):
        print("This goes to debug output")
        print("But this still goes to debug")
    
    print("This goes back to Streamlit")
```

## 2. `st_print` Function

The `st_print` function intelligently formats different data types for Streamlit display.

### String Output

```python
import streamlit as st
from easyst.io.print import st_print

# Simple string output
st_print("Hello, Streamlit!")
st_print("Multiple", "strings", "in", "one", "call")
```

### DataFrame Output

```python
import pandas as pd
import streamlit as st
from easyst.io.print import st_print

# Create a sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
})

# DataFrame will be displayed as an interactive table
st_print("User Data:", df)
st_print(df)  # Just the DataFrame
```

### Dictionary and List Output

```python
import streamlit as st
from easyst.io.print import st_print

# Dictionary output (displayed as JSON)
user_info = {
    'name': 'John Doe',
    'age': 30,
    'skills': ['Python', 'JavaScript', 'SQL']
}
st_print("User Information:", user_info)

# List output (displayed as JSON)
numbers = [1, 2, 3, 4, 5]
st_print("Number sequence:", numbers)
```

### Mixed Data Types

```python
import streamlit as st
import pandas as pd
from easyst.io.print import st_print

# Mixed data types in one print call
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
st_print("DataFrame:", df, "Summary:", df.describe())
st_print("String", 42, [1, 2, 3], {"key": "value"})
```

## 3. Complete Streamlit Application Example

Here's a complete example showing how to use both functions together in a Streamlit app:

```python
import streamlit as st
import pandas as pd
import numpy as np
from easyst.io.print import custom_print, st_print

st.title("easyst Print Examples")

# Example 1: Basic usage
st.header("Basic Print Redirection")
with custom_print(st_print):
    print("This text is redirected to Streamlit!")
    print("You can use print() normally in your code")

# Example 2: DataFrame display
st.header("DataFrame Display")
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100)
})

with custom_print(st_print):
    print("Random Data:")
    print(df.head())
    print("DataFrame Info:")
    print(df.describe())

# Example 3: Complex data structures
st.header("Complex Data Structures")
sample_data = {
    'users': [
        {'name': 'Alice', 'score': 95},
        {'name': 'Bob', 'score': 87},
        {'name': 'Charlie', 'score': 92}
    ],
    'metadata': {
        'total_users': 3,
        'average_score': 91.33
    }
}

with custom_print(st_print):
    print("User Statistics:")
    print(sample_data)

# Example 4: Custom redirect function
st.header("Custom Redirect Function")
def highlight_print(*args, **kwargs):
    """Custom function that highlights important output"""
    for arg in args:
        if isinstance(arg, str) and "important" in arg.lower():
            st.error(arg)
        else:
            st.info(arg)

with custom_print(highlight_print):
    print("This is important information!")
    print("Regular information")
    print("Another important message!")
```

## 4. Advanced Usage Patterns

### Error Handling

```python
import streamlit as st
from easyst.io.print import custom_print, st_print

def safe_print(*args, **kwargs):
    """Safe print function that handles errors gracefully"""
    try:
        st_print(*args, **kwargs)
    except Exception as e:
        st.error(f"Error in print: {e}")

with custom_print(safe_print):
    print("This will work normally")
    # Even if there's an error, it won't crash the app
```

### Conditional Redirection

```python
import streamlit as st
from easyst.io.print import custom_print, st_print

def conditional_print(*args, **kwargs):
    """Print function that changes behavior based on conditions"""
    if st.checkbox("Show debug info"):
        st_print(*args, **kwargs)
    else:
        # Only show important messages
        for arg in args:
            if isinstance(arg, str) and arg.startswith("IMPORTANT:"):
                st_print(arg)

with custom_print(conditional_print):
    print("IMPORTANT: This will always show")
    print("DEBUG: This will only show if checkbox is checked")
    print("Regular message: This will only show if checkbox is checked")
```

## 5. Best Practices

1. **Always use try-finally pattern**: The `custom_print` context manager automatically restores the original print function, but it's good practice to handle exceptions properly.

2. **Choose appropriate redirect functions**: Use `st_print` for general Streamlit output, or create custom functions for specific formatting needs.

3. **Handle different data types**: The `st_print` function automatically handles common data types, but you can create custom functions for specialized formatting.

4. **Performance considerations**: Redirecting print can impact performance in loops or with large amounts of output. Consider using it selectively.

5. **Debugging**: Use `custom_print` to redirect print statements during development and testing, then remove or modify the redirection for production.
