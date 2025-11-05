import streamlit as st
import pandas as pd
from db.connection import execute_query

def reports_page():
    st.header("Reports & Search")

    st.subheader("Search Criminals")
    search_term = st.text_input("Enter Criminal Name or Crime Type")

    if st.button("Search"):
        query = """
            SELECT cr.first_name, cr.last_name, c.type, c.date_committed
            FROM criminals cr
            JOIN crime_involvement ci ON cr.criminal_id = ci.criminal_id
            JOIN crimes c ON ci.crime_id = c.crime_id
            WHERE cr.first_name LIKE %s OR cr.last_name LIKE %s OR c.type LIKE %s
        """
        params = tuple([f"%{search_term}%"] * 3)
        results = execute_query(query, params, fetch_all=True)
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.info("No results found.")
