import sqlite3

connection = sqlite3.connect("data/business.db")

# -------------------------
# Create tables
# -------------------------

connection.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        email TEXT NOT NULL
    )
""")

connection.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
""")

connection.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
""")

connection.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")

# -------------------------
# Insert customers
# -------------------------

connection.executemany("""
    INSERT OR IGNORE INTO customers
    (customer_id, name, city, email)
    VALUES (?, ?, ?, ?)
""", [
    (1, "Rahul Sharma", "Bangalore", "rahul@example.com"),
    (2, "Priya Singh", "Mumbai", "priya@example.com"),
    (3, "Amit Kumar", "Delhi", "amit@example.com"),
    (4, "Neha Gupta", "Bangalore", "neha@example.com"),
    (5, "Rohan Das", "Kolkata", "rohan@example.com"),
    (6, "Sneha Patel", "Mumbai", "sneha@example.com"),
    (7, "Arjun Mehta", "Bangalore", "arjun@example.com"),
    (8, "Ananya Roy", "Delhi", "ananya@example.com"),
])

# -------------------------
# Insert products
# -------------------------

connection.executemany("""
    INSERT OR IGNORE INTO products
    (product_id, name, price)
    VALUES (?, ?, ?)
""", [
    (1, "Laptop", 75000),
    (2, "Monitor", 25000),
    (3, "Keyboard", 3000),
    (4, "Mouse", 1500),
    (5, "Headphones", 5000),
    (6, "Webcam", 4000),
])

# -------------------------
# Insert orders
# -------------------------

connection.executemany("""
    INSERT OR IGNORE INTO orders
    (order_id, customer_id, order_date)
    VALUES (?, ?, ?)
""", [
    (101, 1, "2026-09-01"),
    (102, 2, "2026-09-02"),
    (103, 3, "2026-09-03"),
    (104, 1, "2026-09-05"),
    (105, 4, "2026-09-07"),
    (106, 5, "2026-09-08"),
    (107, 6, "2026-09-10"),
    (108, 7, "2026-09-12"),
    (109, 8, "2026-09-14"),
    (110, 2, "2026-09-15"),
])

# -------------------------
# Insert order items
# -------------------------

connection.executemany("""
    INSERT OR IGNORE INTO order_items
    (order_item_id, order_id, product_id, quantity, unit_price)
    VALUES (?, ?, ?, ?, ?)
""", [
    (1, 101, 1, 1, 75000),
    (2, 101, 3, 2, 3000),

    (3, 102, 2, 1, 25000),
    (4, 102, 5, 2, 5000),

    (5, 103, 1, 1, 75000),
    (6, 103, 4, 2, 1500),

    (7, 104, 2, 2, 25000),
    (8, 104, 6, 1, 4000),

    (9, 105, 5, 1, 5000),
    (10, 105, 4, 2, 1500),

    (11, 106, 1, 1, 75000),
    (12, 106, 6, 1, 4000),

    (13, 107, 3, 3, 3000),
    (14, 107, 5, 1, 5000),

    (15, 108, 2, 1, 25000),
    (16, 108, 4, 2, 1500),

    (17, 109, 1, 1, 75000),
    (18, 109, 5, 1, 5000),

    (19, 110, 2, 1, 25000),
    (20, 110, 6, 2, 4000),
])

connection.commit()
connection.close()

print("Database initialized successfully.")