"""

"""

import sqlite3
import pickle


class PersistentMap:
  def __init__(self, db_path):
    """Initialize the SQLite key-value store."""
    self.db_path = db_path
    self._ensure_table()

  def _ensure_table(self):
    """Ensures that the key-value table exists. Returns True if table already existed."""
    with sqlite3.connect(self.db_path) as conn:
      # Check if table exists
      table_exists = conn.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='kv'"
      ).fetchone()[0] > 0
      
      if not table_exists:
        conn.execute("""
          CREATE TABLE IF NOT EXISTS kv (
            key TEXT PRIMARY KEY,
            value BLOB
          )
        """)
        return False
      return True

  def set(self, key, value):
    """Insert or update a key-value pair."""
    if not isinstance(value, bytes):
      value = pickle.dumps(value)

    with sqlite3.connect(self.db_path) as conn:
      conn.execute(
        "INSERT OR REPLACE INTO kv (key, value) VALUES (?, ?)", (key, value)
      )

  def get(self, key):
    """Retrieve a value by key. Returns None if the key does not exist."""
    with sqlite3.connect(self.db_path) as conn:
      row = conn.execute("SELECT value FROM kv WHERE key=?", (key,)).fetchone()
      if row:
        return pickle.loads(row[0]), False
    return None, True

  def delete(self, key):
    """Delete a key from the database."""
    with sqlite3.connect(self.db_path) as conn:
      conn.execute("DELETE FROM kv WHERE key=?", (key,))

  def keys(self):
    """Return all stored keys."""
    with sqlite3.connect(self.db_path) as conn:
      return [row[0] for row in conn.execute("SELECT key FROM kv").fetchall()]


