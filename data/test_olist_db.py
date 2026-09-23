from app.database.connection import get_connection


connection = get_connection()

tables = connection.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("Tables:")
for table in tables:
    print(table[0])

connection.close()