import streamlit as st
import pandas as pd
from datetime import datetime
from db.connection import execute_query
from utils.helpers import load_data


def core_crud_page(role):
    st.header("Core Record Management (CRUD)")

    table_to_manage = st.selectbox(
        "Select Record Type",
        [
            "Criminals",
            "Crimes",
            "Cases",
            "Police Officers",
            "Victims",
            "Courts",
            "Police Stations"
        ]
    )

    if table_to_manage == "Criminals":
        manage_criminals(role)
    elif table_to_manage == "Crimes":
        manage_crimes(role)
    elif table_to_manage == "Cases":
        manage_cases(role)
    elif table_to_manage == "Police Officers":
        manage_officers(role)
    elif table_to_manage == "Victims":
        manage_victims(role)
    elif table_to_manage == "Courts":
        manage_courts(role)
    elif table_to_manage == "Police Stations":
        manage_stations(role)
    else:
        st.warning("No table selected or table not found.")


def manage_criminals(role):
    st.subheader("Manage Criminals")

    criminals_data = load_data("criminals")
    st.dataframe(pd.DataFrame(criminals_data) if criminals_data else pd.DataFrame())

    # ---------- ADD ----------
    with st.expander("➕ Add Criminal"):
        with st.form(key="criminal_form", clear_on_submit=True):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input("Date of Birth", value=datetime.now().date())
            address = st.text_area("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            status = st.selectbox("Status", ["At Large", "In Custody", "Released", "Deceased"])
            submit_button = st.form_submit_button("Add Criminal")

            if submit_button and first_name and last_name:
                query = """
                    INSERT INTO criminals (first_name, last_name, dob, address, city, state, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                params = (first_name, last_name, dob, address, city, state, status)
                execute_query(query, params)
                st.success("✅ Added new criminal.")
                st.rerun()

    # ---------- DELETE ----------
    if role == "Admin":
        delete_record("criminals", "criminal_id", "first_name", "last_name", "crime_involvement", "criminal_id")


def manage_crimes(role):
    st.subheader("Manage Crimes")

    crimes_data = load_data("crimes")
    st.dataframe(pd.DataFrame(crimes_data) if crimes_data else pd.DataFrame())

    # ---------- ADD ----------
    with st.expander("➕ Add Crime"):
        with st.form(key="crime_form", clear_on_submit=True):
            crime_type = st.text_input("Crime Type")
            description = st.text_area("Description")
            date_committed = st.date_input("Date Committed", value=datetime.now().date())
            location = st.text_input("Location")
            submit_button = st.form_submit_button("Add Crime")

            if submit_button and crime_type:
                query = """
                    INSERT INTO crimes (type, description, date_committed, location)
                    VALUES (%s, %s, %s, %s)
                """
                params = (crime_type, description, date_committed, location)
                execute_query(query, params)
                st.success("✅ Added new crime.")
                st.rerun()

    # ---------- DELETE ----------
    if role == "Admin":
        delete_record("crimes", "crime_id", "type")


def manage_cases(role):
    st.subheader("Manage Cases")

    data = load_data("cases")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    # ---------- ADD ----------
    with st.expander("➕ Add Case"):
        with st.form(key="case_form", clear_on_submit=True):
            crime_id = st.number_input("Crime ID", min_value=1)
            station_id = st.number_input("Station ID", min_value=1)
            court_id = st.number_input("Court ID", min_value=1)
            summary = st.text_area("Summary")
            status = st.selectbox("Status", ["Open", "Closed", "Under Investigation"])
            date_filed = st.date_input("Date Filed", value=datetime.now().date())
            submit_button = st.form_submit_button("Add Case")

            if submit_button:
                query = """
                    INSERT INTO cases (crime_id, station_id, court_id, summary, status, date_filed)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                execute_query(query, (crime_id, station_id, court_id, summary, status, date_filed))
                st.success("✅ Added new case.")
                st.rerun()

    # ---------- DELETE ----------
    if role == "Admin":
        delete_record("cases", "case_id", "summary")


def manage_officers(role):
    st.subheader("Manage Police Officers")

    data = load_data("police_officer")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    # ---------- ADD ----------
    with st.expander("➕ Add Officer"):
        with st.form(key="officer_form", clear_on_submit=True):
            station_id = st.number_input("Station ID", min_value=1)
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            badge_number = st.text_input("Badge Number")
            officer_rank = st.text_input("Rank")
            hire_date = st.date_input("Hire Date", value=datetime.now().date())
            submit_button = st.form_submit_button("Add Officer")

            if submit_button and first_name and badge_number:
                query = """
                    INSERT INTO police_officer (station_id, first_name, last_name, badge_number, officer_rank, hire_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                execute_query(query, (station_id, first_name, last_name, badge_number, officer_rank, hire_date))
                st.success("✅ Added new officer.")
                st.rerun()

    # ---------- DELETE ----------
    if role == "Admin":
        delete_record("police_officer", "officer_id", "first_name", "last_name")


def manage_victims(role):
    st.subheader("Manage Victims")

    data = load_data("victims")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    # ---------- ADD ----------
    with st.expander("➕ Add Victim"):
        with st.form(key="victim_form", clear_on_submit=True):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input("Date of Birth", value=datetime.now().date())
            address = st.text_area("Address")
            phone = st.text_input("Phone Number")
            submit_button = st.form_submit_button("Add Victim")

            if submit_button and first_name:
                query = """
                    INSERT INTO victims (first_name, last_name, dob, address, phone)
                    VALUES (%s, %s, %s, %s, %s)
                """
                execute_query(query, (first_name, last_name, dob, address, phone))
                st.success("✅ Added new victim.")
                st.rerun()

    # ---------- DELETE ----------
    if role == "Admin":
        delete_record("victims", "victim_id", "first_name", "last_name")


def manage_courts(role):
    st.subheader("Manage Courts")

    data = load_data("courts")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    # ---------- ADD ----------
    with st.expander("➕ Add Court"):
        with st.form(key="court_form", clear_on_submit=True):
            name = st.text_input("Court Name")
            court_type = st.selectbox("Type", ["District", "High", "Supreme", "Magistrate"])
            city = st.text_input("City")
            state = st.text_input("State")
            submit_button = st.form_submit_button("Add Court")

            if submit_button and name:
                query = """
                    INSERT INTO courts (name, type, city, state)
                    VALUES (%s, %s, %s, %s)
                """
                execute_query(query, (name, court_type, city, state))
                st.success("✅ Added new court.")
                st.rerun()

    # ---------- DELETE ----------
    if role == "Admin":
        delete_record("courts", "court_id", "name")


def manage_stations(role):
    st.subheader("Manage Police Stations")

    data = load_data("police_station")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    # ---------- ADD ----------
    with st.expander("➕ Add Police Station"):
        with st.form(key="station_form", clear_on_submit=True):
            name = st.text_input("Station Name")
            address = st.text_area("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            submit_button = st.form_submit_button("Add Station")

            if submit_button and name:
                query = """
                    INSERT INTO police_station (name, address, city, state)
                    VALUES (%s, %s, %s, %s)
                """
                execute_query(query, (name, address, city, state))
                st.success("✅ Added new police station.")
                st.rerun()

    # ---------- DELETE ----------
    if role == "Admin":
        delete_record("police_station", "station_id", "name")


# 🔹 Reusable Delete Section
def delete_record(table, id_col, *name_cols, linked_table=None, linked_col=None):
    st.subheader(f"🗑️ Delete from {table.title()} (Admin Only)")
    data = load_data(table)
    if not data:
        st.info(f"No records found in `{table}`.")
        return

    df = pd.DataFrame(data)
    if not df.empty:
        df["display_name"] = df.apply(
            lambda x: " ".join([str(x[col]) for col in name_cols if col in x and x[col]]), axis=1
        )
        record_map = {
            f"{row['display_name']} (ID: {row[id_col]})": row[id_col]
            for _, row in df.iterrows()
        }

        selected = st.selectbox("Select record to delete:", list(record_map.keys()))
        confirm = st.checkbox("Confirm permanent deletion")

        if st.button("Delete Record", type="primary"):
            if confirm:
                if linked_table and linked_col:
                    execute_query(f"DELETE FROM {linked_table} WHERE {linked_col}=%s", (record_map[selected],))
                execute_query(f"DELETE FROM {table} WHERE {id_col}=%s", (record_map[selected],))
                st.success(f"✅ Deleted record: {selected}")
                st.rerun()
            else:
                st.warning("Please confirm before deleting.")
