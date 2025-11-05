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
        show_table_data("cases")
    elif table_to_manage == "Police Officers":
        show_table_data("police_officer")
    elif table_to_manage == "Victims":
        show_table_data("victims")
    elif table_to_manage == "Courts":
        show_table_data("courts")
    elif table_to_manage == "Police Stations":
        show_table_data("police_station")
    else:
        st.warning("No table selected or table not found.")


def show_table_data(table_name):
    """Reusable viewer for tables that don't yet have full CRUD implemented."""
    st.subheader(f"View Data: {table_name}")
    data = load_data(table_name)
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f"No data found in `{table_name}` table.")


def manage_criminals(role):
    st.subheader("Manage Criminals")

    criminals_data = load_data("criminals")
    st.dataframe(pd.DataFrame(criminals_data) if criminals_data else pd.DataFrame())

    # ---------- ADD / UPDATE ----------
    with st.expander("Add or Update Criminal"):
        with st.form(key="criminal_form", clear_on_submit=True):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input("Date of Birth", value=datetime.now().date())
            address = st.text_area("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            status = st.selectbox("Status", ["At Large", "In Custody", "Released", "Deceased"])
            submit_button = st.form_submit_button("Add Criminal")

            if submit_button:
                if not first_name or not last_name:
                    st.warning("First Name and Last Name are required.")
                else:
                    query = """
                        INSERT INTO criminals (first_name, last_name, dob, address, city, state, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    params = (first_name, last_name, dob, address, city, state, status)
                    execute_query(query, params)
                    st.success("Added new criminal.")
                    st.rerun()

    # ---------- DELETE (Admin only) ----------
    if role == "Admin":
        with st.expander("🗑️ Delete Criminal Record (Admin Only)"):
            if criminals_data:
                criminal_map = {
                    f"{c['first_name']} {c['last_name']} (ID: {c['criminal_id']})": c['criminal_id']
                    for c in criminals_data
                }
                selected = st.selectbox("Select Criminal to Delete", list(criminal_map.keys()))
                confirm = st.checkbox("I understand that this will permanently delete the record and related links.")
                if st.button("Delete Criminal", type="primary"):
                    if confirm:
                        execute_query("DELETE FROM crime_involvement WHERE criminal_id=%s", (criminal_map[selected],))
                        execute_query("DELETE FROM criminals WHERE criminal_id=%s", (criminal_map[selected],))
                        st.success(f"Deleted: {selected}")
                        st.rerun()
                    else:
                        st.warning("Please confirm before deleting.")
            else:
                st.info("No criminals found.")


def manage_crimes(role):
    st.subheader("Manage Crimes")

    crimes_data = load_data("crimes")
    st.dataframe(pd.DataFrame(crimes_data) if crimes_data else pd.DataFrame())

    # ---------- ADD / UPDATE ----------
    with st.expander("Add or Update Crime"):
        with st.form(key="crime_form", clear_on_submit=True):
            crime_type = st.text_input("Crime Type")
            description = st.text_area("Description")
            date_committed = st.date_input("Date Committed", value=datetime.now().date())
            location = st.text_input("Location")
            submit_button = st.form_submit_button("Add Crime")

            if submit_button:
                if not crime_type:
                    st.warning("Crime Type is required.")
                else:
                    query = """
                        INSERT INTO crimes (type, description, date_committed, location)
                        VALUES (%s, %s, %s, %s)
                    """
                    params = (crime_type, description, date_committed, location)
                    execute_query(query, params)
                    st.success("Added new crime.")
                    st.rerun()

    # ---------- DELETE (Admin only) ----------
    if role == "Admin":
        with st.expander("🗑️ Delete Crime Record (Admin Only)"):
            if crimes_data:
                crime_map = {
                    f"{c['type']} (ID: {c['crime_id']})": c['crime_id']
                    for c in crimes_data
                }
                selected = st.selectbox("Select Crime to Delete", list(crime_map.keys()))
                confirm = st.checkbox("I understand this will permanently delete the crime.")
                if st.button("Delete Crime", type="primary"):
                    if confirm:
                        execute_query("DELETE FROM crimes WHERE crime_id=%s", (crime_map[selected],))
                        st.success(f"Deleted: {selected}")
                        st.rerun()
                    else:
                        st.warning("Please confirm before deleting.")
            else:
                st.info("No crimes found.")
