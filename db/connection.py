import mysql.connector
import streamlit as st

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Aishwari@2006"   # your MySQL password
DB_NAME = "criminal_db"


def get_db_connection():
    """Establish connection to MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aishwari@2006",
            database="criminal_db"
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Execute a query safely with error handling."""
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid or cursor.rowcount

        return result

    except mysql.connector.Error as e:
        st.error(f"SQL Error: {e}")
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
