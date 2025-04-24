# jsonschema_explorer

A simple Python tool to parse a JSON object and explore its schema, displaying the data types in a readable format.

**Note**: This package only analyzes the **first JSON object** in a list of JSON objects. It will display how many JSON objects are in the list with a field called "_length".

## Installation

To install, use pip:

```bash
pip install jsonschema_explorer


```

# example use case 

```python

data = [{
    "name": "Alice",
    "age": 20,
    "address": {
        "street": "789 Oak St",
        "city": "Sometown",
        "postcode": "ST1 0AL"
    }},
    {"name": "Hugo",
    "age": 35,
    "address": {
        "street": "123 Maple Rd",
        "city": "Atown",
        "postcode": "AT1 9LF"
    }}
]

from jsonschema_explorer import schema

data_schema = schema(data)

print(data_schema)
```

# Output
```bash

[
   {
      "name": "str",
      "age": "int",
      "address": {
         "street": "str",
         "city": "str",
         "postcode": "str"
      }
   },
   {
      "_length": 2
   }
]

```