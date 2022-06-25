import sqlite3

conn = sqlite3.connect("safe.db")

try:
    conn.execute("DROP DATABASE safe.db")
    print("Success")
except:
    print("error")