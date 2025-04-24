diskoize:memoize::disk:memory

# What is this

Often when I use @functools.lru_cache I find that the cache is erased between python process restarts. This library is the fix!

```bash
import diskoize
import requests

@diskoize.diskoize("scrape_cache.db")
def scrape(url):
  return requests.request(url)


scrape("google.com") # <-- will run only once, even after rerunning this script.
```

You need to manually delete the cache if you change the function's input-output behavior.



# Tests

We use pytest for testing. To run the tests, you can use the following command:

```bash
pytest
```
This will run all the tests in the `tests` directory. You can also run a specific test file by providing the path to the file:

```bash
pytest tests/test_file.py
```

# Development

Make a temporary pip install: pip install -e .
Now you can use the library from any python script, and edits to the local diskoize/ folder will be reflected.

# Remarks

* There is a tension between making this library understandable and making it easy to use.
  -- we always give the option of explicitly naming the backing sqlite database file.
  -- for autonaming, we currently create or reuse a file in the system temp directory which is based 
  based on the diskoized function's __name__. It is up to the user to delete invalidated caches. So autonaming should probably only be used for quick-and-dirty experiments where we don't expect to come back to the code after a long while. 


# TODOs

* add option in_memory (default False) to store the cache in memory, always with persistent backing.
* make the tests actually test separate processes accessing the same cache
* add methods for interacting with the cache
* add more examples
* add flush() method, and a lru_cache to support it
* fix _make_key
