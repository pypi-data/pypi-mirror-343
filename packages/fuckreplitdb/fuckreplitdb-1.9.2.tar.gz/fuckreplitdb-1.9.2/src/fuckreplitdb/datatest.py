
from __init__ import FuckReplitDB
import orjson
import os

db = FuckReplitDB("test_db.json")

# Test 1: Simple key-value
db["key"] = "value"
assert os.path.exists("test_db.json")
with open("test_db.json", "rb") as f:
    data = orjson.loads(f.read())
    assert data["key"] == "value"

# Test 2: Nested dict
db["nested"]["a"]["b"] = 42
with open("test_db.json", "rb") as f:
    data = orjson.loads(f.read())
    assert data["nested"]["a"]["b"] == 42

# Test 3: Nested list
db["list"] = [1, {"x": "y"}, [2, 3]]
db["list"][1]["x"] = "z"
print(type(db["list"]))
with open("test_db.json", "rb") as f:
    data = orjson.loads(f.read())
    assert data["list"][1]["x"] == "z"

