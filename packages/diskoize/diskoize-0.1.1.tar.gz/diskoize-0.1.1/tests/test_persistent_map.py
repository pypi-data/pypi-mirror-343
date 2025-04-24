# filepath: tests/test_persistent_map.py
import os
import tempfile
import pytest
from diskoize import PersistentMap

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)

def test_set_get(temp_db):
    pm = PersistentMap(temp_db)
    pm.set("key1", "value1")
    result, miss = pm.get("key1")
    assert result == "value1"
    assert miss == False

def test_get_missing(temp_db):
    pm = PersistentMap(temp_db)
    result, miss = pm.get("nonexistent")
    assert result is None
    assert miss == True

def test_delete(temp_db):
    pm = PersistentMap(temp_db)
    pm.set("key1", "value1")
    pm.delete("key1")
    result, miss = pm.get("key1")
    assert miss == True

def test_keys(temp_db):
    pm = PersistentMap(temp_db)
    pm.set("key1", "value1")
    pm.set("key2", "value2")
    keys = pm.keys()
    assert sorted(keys) == ["key1", "key2"]
