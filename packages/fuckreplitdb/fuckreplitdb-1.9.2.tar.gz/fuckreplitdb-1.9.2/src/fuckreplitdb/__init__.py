


from collections.abc import MutableMapping
import orjson
import os
import threading
import tempfile
from collections.abc import MutableSequence


class _NestedDict(dict):
    def __init__(self, *args, **kwargs):
        self._parent = kwargs.pop('_parent', None)
        self._key = kwargs.pop('_key', None)
        self._root = kwargs.pop('_root', None)
        self._skip_save = kwargs.pop('_skip_save', False)
        dict.__init__(self, *args, **kwargs)
        if self._root is not None and not self._skip_save:
            self._root._enable_saves_recursively(self)
        
    def __getitem__(self, key):
        if key not in self:
            self[key] = _NestedDict(_parent=self, _key=key, _root=self._root, _skip_save=False)
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        key = str(key)
        if isinstance(value, dict) and not isinstance(value, _NestedDict):
            value = _NestedDict(value, _parent=self, _key=key, _root=self._root, _skip_save=False)
        elif isinstance(value, list):
            value = _NestedList(value, _parent=self, _key=key, _root=self._root, _skip_save=False)
        dict.__setitem__(self, key, value)
        if not self._skip_save:
            self._save_root()

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default
    
    def set(self, key, value):
        self[key] = value
        return value
        
    def _save_root(self):
        if self._skip_save:
            return
        if self._root is not None:
            self._root._save()
        elif self._parent is not None:
            self._parent._save_root()
            
    def to_dict(self):
        result = {}
        for k, v in self.items():
            if isinstance(v, (_NestedDict, _NestedList)):
                result[k] = v.to_dict()
            else:
                result[k] = v
        return result
        
    def keys(self):
        return dict.keys(self)
        
    def values(self):
        return dict.values(self)
        
    def items(self):
        return dict.items(self)
        
    def __iter__(self):
        return dict.__iter__(self)
        
    def __delitem__(self, key):
        dict.__delitem__(self, key)
        if not self._skip_save:
            self._save_root()

class _NestedList(MutableSequence):
    def __init__(self, initial_list=None, _parent=None, _key=None, _root=None, _skip_save=False):
        self._list = list(initial_list or [])
        self._parent = _parent
        self._key = _key
        self._root = _root
        self._skip_save = _skip_save
        self._convert_nested()
        if self._root is not None and not self._skip_save:
            self._root._enable_saves_recursively(self)

    def _convert_nested(self):
        for i, item in enumerate(self._list):
            if isinstance(item, dict) and not isinstance(item, _NestedDict):
                self._list[i] = _NestedDict(item, _parent=self, _key=i, _root=self._root, _skip_save=self._skip_save)
            elif isinstance(item, list):
                self._list[i] = _NestedList(item, _parent=self, _key=i, _root=self._root, _skip_save=self._skip_save)

    def _save_root(self):
        if self._skip_save:
            return
        if self._root is not None:
            self._root._save()
        elif self._parent is not None:
            self._parent._save_root()

    def to_dict(self):
        return [v.to_dict() if isinstance(v, (_NestedDict, _NestedList)) else v for v in self._list]

    def __getitem__(self, index):
        return self._list[index]

    def __delitem__(self, index):
        del self._list[index]
        if not self._skip_save:
            self._save_root()

    def __len__(self):
        return len(self._list)

    def __setitem__(self, index, value):
        if isinstance(value, dict) and not isinstance(value, _NestedDict):
            value = _NestedDict(value, _parent=self, _key=index, _root=self._root, _skip_save=False)
        elif isinstance(value, list):
            value = _NestedList(value, _parent=self, _key=index, _root=self._root, _skip_save=False)
        self._list[index] = value
        if not self._skip_save:
            self._save_root()

    def insert(self, index, value):
        if isinstance(value, dict) and not isinstance(value, _NestedDict):
            value = _NestedDict(value, _parent=self, _key=index, _root=self._root, _skip_save=False)
        elif isinstance(value, list):
            value = _NestedList(value, _parent=self, _key=index, _root=self._root, _skip_save=False)
        self._list.insert(index, value)
        if not self._skip_save:
            self._save_root()


class FuckReplitDB(MutableMapping):
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.lock = threading.RLock()
        self.store = None
        self._loading = True
        self._load()
        self._loading = False
        
    def _load(self):
        with self.lock:
            if os.path.exists(self.filename):
                try:
                    with open(self.filename, 'rb') as f:
                        data = orjson.loads(f.read())
                        self.store = self._to_nested(data)
                except (orjson.JSONDecodeError, FileNotFoundError):
                    self.store = _NestedDict(_root=self, _skip_save=True)
            else:
                self.store = _NestedDict(_root=self, _skip_save=True)

            if self.store is not None:
                self._enable_saves_recursively(self.store)
                
    def _enable_saves_recursively(self, obj):
        if isinstance(obj, _NestedDict):
            obj._skip_save = False
            for value in obj.values():
                self._enable_saves_recursively(value)
        elif isinstance(obj, _NestedList):
            obj._skip_save = False
            for value in obj:
                self._enable_saves_recursively(value)
                
    def _save(self):
        if self._loading:
            return
            
        with self.lock:
            if self.store is None:
                return
                
            dir_name = os.path.dirname(self.filename)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
                
            with tempfile.NamedTemporaryFile('wb', dir=dir_name or '.', delete=False) as tmp_file:
                json_bytes = orjson.dumps(
                    self.store.to_dict(),
                    option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
                )
                tmp_file.write(json_bytes)
                temp_name = tmp_file.name
            os.replace(temp_name, self.filename)
            
    def _to_nested(self, d):
        if isinstance(d, dict):
            result = _NestedDict(_root=self, _skip_save=True)
            for k, v in d.items():
                k = str(k)
                result[k] = self._to_nested(v)
            return result
        elif isinstance(d, list):
            return _NestedList(d, _root=self, _skip_save=True)
        return d

    def __len__(self):
        with self.lock:
            if self.store is None:
                return 0
            return len(self.store)

    def get(self, key, default=None):
        with self.lock:
            if self.store is None:
                return default
            return self.store.get(key, default)
    
    def set(self, key, value):
        with self.lock:
            if self.store is None:
                self.store = _NestedDict(_root=self)
            self.store[key] = value
            self._save()
            return value
            
    def __iter__(self):
        with self.lock:
            if self.store is None:
                return iter([])
            return iter(self.store)
        
    def __getitem__(self, key):
        with self.lock:
            if self.store is None:
                raise KeyError(f"Key '{key}' not found - database not loaded")
            return self.store[key]
            
    def __setitem__(self, key, value):
        with self.lock:
            if self.store is None:
                self.store = _NestedDict(_root=self)
            self.store[key] = value
            self._save()
            
    def __delitem__(self, key):
        with self.lock:
            if self.store is None:
                raise KeyError(f"Key '{key}' not found - database not loaded")
            del self.store[key]
            self._save()
            
    def __contains__(self, key):
        with self.lock:
            if self.store is None:
                return False
            return key in self.store
            
    def keys(self):
        with self.lock:
            if self.store is None:
                return []
            return self.store.keys()
            
    def values(self):
        with self.lock:
            if self.store is None:
                return []
            return self.store.values()
            
    def items(self):
        with self.lock:
            if self.store is None:
                return []
            return self.store.items()



        
