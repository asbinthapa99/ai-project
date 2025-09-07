import sqlite3, os

BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, "app.db")

schema = """
-- users
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL, -- NOTE: Plain text for demo; discuss hashing in report
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- attempts
CREATE TABLE IF NOT EXISTS attempts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  score INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.executescript(schema)
    con.commit()
    con.close()
    print("Database initialised:", DB)

if __name__ == "__main__":
    main()
