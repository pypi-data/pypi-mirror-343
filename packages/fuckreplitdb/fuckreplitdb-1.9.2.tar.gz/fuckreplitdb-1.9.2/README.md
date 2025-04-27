
# General Information and Usage

## Overview

The `FuckReplitDB` class is designed to function as a simple drop-in replacement for Replit DB (or any other key-value store), similar to how you might use a dictionary, but with persistent file-backed storage. It stores data in a JSON-like structure on disk and offers both basic key-value operations and the ability to handle nested dictionaries, making it ideal for use cases where you need to persist data in a file but want a simple API for access and modification.

### **Key Features**

- **Drop-in Replacement**: The class is designed to work like a Python dictionary, so you can directly replace a dictionary in your code with an instance of `FuckReplitDB` without changing much of the underlying logic. It supports all the basic dictionary operations like `get`, `set`, `delete`, and checking for key existence.

- **Persistent Storage**: The data is stored on disk in a file using the `orjson` format, allowing you to persist data between application runs. This makes it a lightweight alternative to more complex databases for simple applications.

- **Nested Data**: With support for nested dictionaries, the class allows you to easily represent and manipulate complex hierarchical data structures, making it useful for storing configuration settings, user data, or any other type of structured data.

- **Thread-Safe**: The class uses `threading.Lock` to ensure thread-safe operations, so it can be used in multi-threaded environments without the risk of data corruption.

- **Simple API**: The class exposes an intuitive dictionary-like API, making it easy to use and understand.

---

## Drop-in Replacement

One of the core design principles behind `FuckReplitDB` is that it should be as simple to use as a Python dictionary. Here's a quick comparison of using `FuckReplitDB` versus a regular dictionary:

### **Using Python Dictionary:**

```python
# Using a regular dictionary
my_dict = {}

# Setting a value
my_dict['name'] = 'Alice'

# Getting a value
print(my_dict.get('name'))  # Output: Alice

# Deleting a key
del my_dict['name']
```

### **Using `FuckReplitDB`:**

```python
# Using FuckReplitDB for persistent storage
db = FuckReplitDB('data.json')

# Setting a value
db.set('name', 'Alice')

# Getting a value
print(db.get('name'))  # Output: Alice

# Deleting a key
del db['name']
```

As you can see, the usage of `FuckReplitDB` is nearly identical to using a regular dictionary. The key difference is that `FuckReplitDB` persists its data to a file, and operations are thread-safe.

---

## Advanced Usage

### **Working with Nested Data**

`FuckReplitDB` supports nested dictionaries using the `NestedDict` class, which allows you to work with hierarchical data structures. For example:

```python
# Using nested dictionaries
db['user'] = {'name': 'Bob', 'details': {'age': 30, 'city': 'New York'}}

# Accessing nested data
print(db['user']['name'])  # Output: Bob
print(db['user']['details']['age'])  # Output: 30

# Modifying nested data
db['user']['details']['city'] = 'San Francisco'

# Deleting nested data
del db['user']['details']['city']
```

This feature allows you to manipulate data that is structured in multiple levels, like a user profile with personal information and settings.

---

## Basic Operations

### **Setting a Key-Value Pair**

You can set values using `db.set(key, value)` or using dictionary-style syntax:

```python
db.set('age', 25)       # Setting with set()
db['name'] = 'Alice'    # Setting with dictionary-style assignment
```

### **Getting a Value**

You can retrieve a value using the `get()` method or the dictionary-style `[]` operator:

```python
print(db.get('age'))       # Using get()
print(db['name'])          # Using dictionary-style access
```

### **Checking for Existence**

Check if a key exists with the `in` operator, just like a regular dictionary:

```python
if 'age' in db:
    print('Age is set')
```

### **Deleting a Key**

Use `del` to remove a key from the database:

```python
del db['age']
```

### **Iterating over Keys**

You can iterate over the keys in the database using `db.keys()` or by directly iterating over the object:

```python
for key in db:
    print(key)
```

---

## Thread Safety

`FuckReplitDB` ensures that multiple threads accessing the database simultaneously do not cause data corruption or race conditions. The database uses a lock (`threading.Lock`) around all file operations to make sure that only one thread can read or write to the file at a time.

For example, if you have multiple threads accessing and modifying the database:

```python
import threading

def set_data():
    db.set('name', 'Alice')

threads = []
for _ in range(10):
    t = threading.Thread(target=set_data)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

This is thread-safe because each file operation is locked, preventing concurrent writes or reads that could cause data inconsistency.

---

## Conclusion

The `FuckReplitDB` class is an easy-to-use, lightweight, and thread-safe key-value store that can be used as a simple drop-in replacement for Python's built-in dictionary when you need persistent storage. It supports all basic dictionary operations, works with nested data structures, and handles concurrency without any extra complexity on your part. I made this because I wrote an app with Replit DB that got a bit too big for a complete rewrite (oops) so that's where the name came from.

