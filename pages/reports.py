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
            LEFT JOIN crime_involvement ci ON cr.criminal_id = ci.criminal_id
            LEFT JOIN crimes c ON ci.crime_id = c.crime_id
            WHERE cr.first_name LIKE %s OR cr.last_name LIKE %s OR c.type LIKE %s
        """
        params = tuple([f"%{search_term}%"] * 3)
        results = execute_query(query, params, fetch_all=True)
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.info("No results found.")

    # ------------------- FILTER / REPORT SECTION -------------------
    st.subheader("📑 Filtered Reports")

    report_type = st.selectbox(
        "Select a Report Type:",
        [
            "List all criminals in a specific city",
            "List all cases handled by a specific officer",
            "List cases per police station"
        ]
    )

    df = pd.DataFrame()

    # 1️⃣ Criminals by City
    if report_type == "List all criminals in a specific city":
        city = st.text_input("Enter City Name")
        if st.button("Generate City Report"):
            query = "SELECT first_name, last_name, city, state, status FROM criminals WHERE LOWER(TRIM(city)) LIKE LOWER(%s)"
            data = execute_query(query, (f"%{city.strip()}%",), fetch_all=True)
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info(f"No criminals found in '{city}'.")

    # 2️⃣ Cases by Officer
    elif report_type == "List all cases handled by a specific officer":
        officers = execute_query(
            "SELECT officer_id, CONCAT(first_name, ' ', last_name, ' (', badge_number, ')') AS officer_name FROM police_officer ORDER BY first_name",
            fetch_all=True
        )
        if officers:
            officer_map = {o["officer_name"]: o["officer_id"] for o in officers}
            selected_officer = st.selectbox("Select Officer", list(officer_map.keys()))
            if st.button("Generate Officer Report"):
                query = """
                    SELECT 
                        c.case_id AS CaseID,
                        c.summary AS Summary,
                        c.status AS Status,
                        c.date_filed AS DateFiled,
                        ps.name AS PoliceStation
                    FROM cases c
                    JOIN case_assignment ca ON c.case_id = ca.case_id
                    JOIN police_officer po ON ca.officer_id = po.officer_id
                    JOIN police_station ps ON c.station_id = ps.station_id
                    WHERE po.officer_id = %s;
                """
                data = execute_query(query, (officer_map[selected_officer],), fetch_all=True)
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info(f"No cases found for {selected_officer}.")
        else:
            st.warning("No officers available in database.")

    # 3️⃣ Cases per Police Station
    elif report_type == "List cases per police station":
        if st.button("Generate Station Report"):
            query = """
                SELECT 
                    ps.name AS PoliceStation,
                    ps.city AS City,
                    COUNT(c.case_id) AS TotalCases,
                    SUM(CASE WHEN c.status = 'Open' THEN 1 ELSE 0 END) AS OpenCases,
                    SUM(CASE WHEN c.status = 'Closed' THEN 1 ELSE 0 END) AS ClosedCases
                FROM cases c
                JOIN police_station ps ON c.station_id = ps.station_id
                GROUP BY ps.station_id
                ORDER BY TotalCases DESC;
            """
            data = execute_query(query, fetch_all=True)
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No case data found for police stations.")

    # ------------------- EXPORT OPTION -------------------
    if not df.empty:
        st.download_button(
            label="⬇️ Export Report to CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"{report_type.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )