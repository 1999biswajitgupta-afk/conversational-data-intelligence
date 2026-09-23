from app.database.connection import get_connection


def get_all_customers():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    connection.close()

    return customers

def get_customers_by_city(city: str):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE city = ?",
        (city,)
    )

    customers = cursor.fetchall()

    connection.close()

    return customers