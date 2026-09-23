def validate_sql(sql: str) -> str:
    normalized_sql = sql.strip().lower()

    if not normalized_sql.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
    ]

    for keyword in forbidden_keywords:
        if keyword in normalized_sql:
            raise ValueError(f"Forbidden SQL operation: {keyword}")

    return sql