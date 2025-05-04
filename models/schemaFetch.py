import sqlite3

def fetchSchema():
    conn = sqlite3.connect('./data/dataset.db')
    cur = conn.cursor()

    # Step 1: Get all user table names (excluding system tables)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cur.fetchall()]
    dbSchema = ''
    # Step 2: Fetch and print the CREATE TABLE statement for each table
    for table in tables:
        cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
        schema = cur.fetchone()[0]
        dbSchema += f"Schema for table {table}:\n{schema}\n"
        # print(f"Schema for table {table}:\n{schema}\n")

    cur.close()
    conn.close()
    return dbSchema
