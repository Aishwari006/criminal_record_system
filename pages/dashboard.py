import streamlit as st
import pandas as pd
import plotly.express as px
from db.connection import execute_query

def dashboard_page():
    st.header("🚓 Criminal Record Dashboard")

    # KPIs
    try:
        col1, col2, col3, col4, col5 = st.columns(5)
        total_criminals = execute_query("SELECT COUNT(*) as count FROM criminals", fetch_one=True)['count']
        total_cases = execute_query("SELECT COUNT(*) as count FROM cases", fetch_one=True)['count']
        open_cases = execute_query("SELECT COUNT(*) as count FROM cases WHERE status = 'Open'", fetch_one=True)['count']
        total_officers = execute_query("SELECT COUNT(*) as count FROM police_officer", fetch_one=True)['count']
        total_crimes = execute_query("SELECT COUNT(*) as count FROM crimes", fetch_one=True)['count']

        col1.metric("Total Criminals", total_criminals)
        col2.metric("Total Cases", total_cases)
        col3.metric("Open Cases", open_cases)
        col4.metric("Total Officers", total_officers)
        col5.metric("Total Crimes", total_crimes)
    except Exception:
        st.warning("Could not load dashboard KPIs. Is the database populated?")

    st.divider()

    # Charts
    st.subheader("Visual Reports")
    col1, col2 = st.columns(2)

    with col1:
        data = execute_query("SELECT status, COUNT(*) as count FROM cases GROUP BY status", fetch_all=True)
        if data:
            df = pd.DataFrame(data)
            fig = px.pie(df, names='status', values='count', title='Case Status Distribution')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        data = execute_query("""
            SELECT p.city, COUNT(c.crime_id) as crime_count
            FROM crimes c
            JOIN cases ca ON c.crime_id = ca.crime_id
            JOIN police_station p ON ca.station_id = p.station_id
            GROUP BY p.city
        """, fetch_all=True)
        if data:
            df = pd.DataFrame(data)
            fig = px.bar(df, x='city', y='crime_count', title='Crimes per City')
            st.plotly_chart(fig, use_container_width=True)
