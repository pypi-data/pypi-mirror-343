
from __init__ import FuckReplitDB
import os
import threading
import time
from collections.abc import MutableMapping
import pytest

# Test file
DB_FILE = "test_db.json"

def setup_db():
    # Clean up any existing test file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    return FuckReplitDB(filename=DB_FILE)

def test_is_dict_like():
    db = setup_db()
    assert isinstance(db, MutableMapping)
    assert hasattr(db, '__getitem__')
    assert hasattr(db, '__setitem__')
    assert hasattr(db, '__delitem__')
    assert hasattr(db, '__iter__')
    assert hasattr(db, '__len__')
    assert hasattr(db, '__contains__')

def test_basic_operations():
    db = setup_db()
    
    # Set and get
    db['key1'] = 'value1'
    assert db['key1'] == 'value1'
    assert db.get('key1') == 'value1'
    
    # Update
    db['key1'] = 'value2'
    assert db['key1'] == 'value2'
    
    # Delete
    del db['key1']
    assert 'key1' not in db
    assert db.get('key1') is None
    
    # Contains
    db['key2'] = 'value2'
    assert 'key2' in db
    assert 'key3' not in db

def test_nested_dict():
    db = setup_db()
    
    # Nested dictionary
    db['nested']['a']['b'] = 42
    assert db['nested']['a']['b'] == 42
    assert db['nested'].to_dict() == {'a': {'b': 42}}
    
    # Nested list
    db['nested']['list'] = [1, {'x': 'y'}, [3, 4]]
    assert db['nested']['list'][0] == 1
    assert db['nested']['list'][1]['x'] == 'y'
    assert db['nested']['list'][2][1] == 4
    
    # Modify nested
    db['nested']['list'][1]['x'] = 'z'
    assert db['nested']['list'][1]['x'] == 'z'

def test_persistence():
    db = setup_db()
    
    # Set some data
    db['key1'] = 'value1'
    db['nested'] = {'a': 1, 'b': [2, 3]}
    
    # Create new instance
    db2 = FuckReplitDB(filename=DB_FILE)
    
    # Verify data persisted
    assert db2['key1'] == 'value1'
    assert db2['nested']['a'] == 1
    assert db2['nested']['b'][1] == 3

def test_iteration():
    db = setup_db()
    
    # Set multiple keys
    data = {'a': 1, 'b': 2, 'c': 3}
    for k, v in data.items():
        db[k] = v
    
    # Test iteration
    assert sorted(list(db)) == ['a', 'b', 'c']
    assert sorted(db.keys()) == ['a', 'b', 'c']
    assert sorted(db.values()) == [1, 2, 3]
    assert sorted(db.items()) == [('a', 1), ('b', 2), ('c', 3)]

def test_thread_safety():
    db = setup_db()
    results = []
    
    def writer_thread(key, value, iterations):
        for _ in range(iterations):
            db[key] = value
            time.sleep(0.001)
    
    def reader_thread(key, iterations):
        for _ in range(iterations):
            try:
                results.append(db[key])
            except KeyError:
                results.append(None)
            time.sleep(0.001)
    
    # Start multiple threads
    threads = [
        threading.Thread(target=writer_thread, args=('test', i, 100))
        for i in range(5)
    ] + [
        threading.Thread(target=reader_thread, args=('test', 100))
        for _ in range(5)
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Verify no crashes and some reads succeeded
    assert len(results) == 500
    assert any(r is not None for r in results)

def test_edge_cases():
    db = setup_db()
    
    # Empty database
    assert len(db) == 0
    assert list(db) == []
    
    # None values
    db['none'] = None
    assert db['none'] is None
    
    # Complex keys
    db[123] = 'number'
    assert db['123'] == 'number'
    
    # Large data
    large_data = {'x': list(range(1000))}
    db['large'] = large_data
    assert db['large']['x'][999] == 999
    
    # Delete non-existent key
    with pytest.raises(KeyError):
        del db['nonexistent']

def test_file_corruption():
    db = setup_db()
    db['key'] = 'value'
    
    # Corrupt the file
    with open(DB_FILE, 'w') as f:
        f.write('invalid json')
    
    # Should handle corruption gracefully
    db2 = FuckReplitDB(filename=DB_FILE)
    assert len(db2) == 0

if __name__ == '__main__':
    pytest.main([__file__])



    
