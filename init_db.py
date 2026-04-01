import sqlite3

def init_db():
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()
    with open("schema.sql") as f:
        c.executescript(f.read())
    conn.commit()
    conn.close()
    print("DB initialized")

if __name__ == "__main__":
    init_db()
