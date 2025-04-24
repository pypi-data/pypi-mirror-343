# filepath: tests/test_diskoize.py
import os
import tempfile
import pytest
from diskoize import diskoize, _make_key

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)

def test_make_key():
    key = _make_key((1, "test"), {"a": 2, "b": "hello"})
    assert "1" in key
    assert "test" in key
    assert "a=2" in key
    assert "b='hello'" in key

def test_diskoize_caching(temp_db):
    call_count = 0
    
    @diskoize(temp_db)
    def test_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call - should execute function
    assert test_func(5) == 10
    assert call_count == 1
    
    # Second call - should use cache
    assert test_func(5) == 10
    assert call_count == 1
    
    # Different arg - should execute function
    assert test_func(7) == 14
    assert call_count == 2

def test_none_return_value(temp_db):
    call_count = 0
    
    @diskoize(temp_db)
    def returns_none(x):
        nonlocal call_count
        call_count += 1
        return None
    
    # First call - should execute function
    assert returns_none(1) is None
    assert call_count == 1
    
    # Second call - should use cache
    assert returns_none(1) is None
    assert call_count == 1
