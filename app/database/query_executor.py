from app.database.connection import get_connection


def execute_query(sql: str):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    connection.close()

    return results