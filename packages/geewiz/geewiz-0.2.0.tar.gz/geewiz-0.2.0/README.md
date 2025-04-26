# Geewiz

Python SDK for interacting with geewiz.

## Installation

```sh
pip install geewiz
```

## Usage

### Simple

```python
import geewiz

geewiz.set(title="my app")

geewiz.var.my_var = "my value"

username = geewiz.card("get-username")
```

### Showing a card

```python
# show a card with the id "my_card_id"
result = geewiz.card("my_card_id")

# show a card with the id "my_card_id" and override `type` and `items` parameters
result = geewiz.card("my_card_id", type="selectOne", items=["one", "two", "three"])

# show a card with no id
result = geewiz.card(type="selectOne", items=["one", "two", "three"])

# if card doesn't have an input, or you don't need the input, you don't need to save the return value
geewiz.card("my_card_without_input")
```

### Setting a variable

```python
geewiz.var.my_var = "my value"
geewiz.var["my-var-with-dashes"] = "my value"

# you can use the variables you've set
geewiz.var.username = load_username_from_db

if geewiz.vars.username == 'nicholaides':
  # ...
```

### Setting the title of the app

```python
geewiz.set(title="my app")
```

### Getting user config

```python
user_id = geewiz.get_user_config("user_id") # will return None if config value is not set
```

### Advanced: using a non-global client

This can be useful for mocking or testing code that uses Geewiz.

```python
from geewiz.client import GeewizClient

geewiz = GeewizClient()

geewiz.set(title="my app")
geewiz.var.my_var = "my value"
result = geewiz.card("my_card_id")
```
