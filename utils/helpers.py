from db.connection import execute_query

def load_data(table_name):
    """Loads all data from a specified table."""
    return execute_query(f"SELECT * FROM {table_name}", fetch_all=True)


def get_dropdown_data(table, id_col, name_col, order_by=None):
    """Fetch dropdown-friendly data (id:name)."""
    order_clause = f"ORDER BY {order_by}" if order_by else f"ORDER BY {name_col}"
    data = execute_query(f"SELECT {id_col}, {name_col} FROM {table} {order_clause}", fetch_all=True)
    return {item[name_col]: item[id_col] for item in data} if data else {}


def get_full_dropdown_data(query, id_col, name_col):
    """Fetch data using a custom query."""
    data = execute_query(query, fetch_all=True)
    return {item[name_col]: item[id_col] for item in data} if data else {}
