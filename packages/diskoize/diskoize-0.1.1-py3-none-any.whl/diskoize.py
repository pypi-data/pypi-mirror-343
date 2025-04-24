"""
 A decorator to cache the results of a function on disk.
 
Minimal example:

import diskoize from diskoize

@diskoize("/tmp/expensive_computation.db")
def expensive_computation():
  print("Computing")
  return 17

Running this example once will print "Computing" and return 17. Running it again will return 17 without printing anything.

"""

import functools
import tempfile
import os

from persistent_map import PersistentMap

# From functools.
def _make_key(args, kwds):
  """Generate a cache key based on function arguments."""
  key_parts = list(map(repr, args)) + [f"{k}={repr(v)}" for k, v in kwds.items()]
  return "_".join(key_parts)


def diskoize(db_path=None):
  def decorator(func):
    resolved_path = db_path or os.path.join(tempfile.gettempdir(), f"diskoize_cache_{func.__name__}.db")
    cache = PersistentMap(resolved_path)
    @functools.wraps(func)
    def wrapper(*args, **kwds):
      key = _make_key(args, kwds)
      result, miss = cache.get(key)
      if not miss:
        return result
      result = func(*args, **kwds)
      cache.set(key, result)
      return result
    return wrapper
  return decorator