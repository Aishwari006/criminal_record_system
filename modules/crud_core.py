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

    handlers = {
        "Criminals": manage_criminals,
        "Crimes": manage_crimes,
        "Cases": manage_cases,
        "Police Officers": manage_officers,
        "Victims": manage_victims,
        "Courts": manage_courts,
        "Police Stations": manage_stations
    }

    if table_to_manage in handlers:
        handlers[table_to_manage](role)
    else:
        st.warning("No table selected or table not found.")


# 🔹------------------ COMMON DELETE SECTION ------------------🔹
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


# 🔹------------------ UNIVERSAL UPDATE FUNCTION ------------------🔹
def update_record(table_name, id_col, role):
    data = load_data(table_name)
    if not data:
        st.info(f"No records available to update in `{table_name}`.")
        return

    df = pd.DataFrame(data)
    record_map = {f"{table_name.title()} ID {r[id_col]}": r[id_col] for r in data}
    selected = st.selectbox("Select record to update:", list(record_map.keys()))

    if selected:
        rec_id = record_map[selected]
        record = next((r for r in data if r[id_col] == rec_id), None)
        if not record:
            st.warning("Record not found.")
            return

        with st.form(key=f"update_{table_name}_{rec_id}", clear_on_submit=False):
            editable_fields = {
                k: v for k, v in record.items()
                if k != id_col and not k.endswith("_id")  # exclude PKs + FKs
            }

            new_values = {}
            for field, value in editable_fields.items():
                if isinstance(value, str):
                    new_values[field] = st.text_input(field.replace("_", " ").title(), value)
                elif isinstance(value, datetime):
                    new_values[field] = st.date_input(field.replace("_", " ").title(), value)
                elif isinstance(value, (int, float)):
                    new_values[field] = st.number_input(field.replace("_", " ").title(), value=value)
                else:
                    new_values[field] = st.text_input(field.replace("_", " ").title(), str(value) if value else "")

            submitted = st.form_submit_button("Update Record")
            if submitted:
                set_clause = ", ".join([f"{col}=%s" for col in new_values.keys()])
                params = list(new_values.values()) + [rec_id]
                query = f"UPDATE {table_name} SET {set_clause} WHERE {id_col}=%s"
                execute_query(query, tuple(params))
                st.success("✅ Record updated successfully!")
                st.rerun()


# 🔹------------------ INDIVIDUAL TABLE HANDLERS ------------------🔹
def manage_criminals(role):
    st.subheader("Manage Criminals")
    data = load_data("criminals")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    # Add
    with st.expander("➕ Add Criminal"):
        with st.form("add_criminal", clear_on_submit=True):
            first = st.text_input("First Name")
            last = st.text_input("Last Name")
            dob = st.date_input("DOB", datetime.now().date())
            addr = st.text_area("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            status = st.selectbox("Status", ["At Large", "In Custody", "Released", "Deceased"])
            if st.form_submit_button("Add"):
                execute_query(
                    "INSERT INTO criminals (first_name,last_name,dob,address,city,state,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (first, last, dob, addr, city, state, status)
                )
                st.success("✅ Added criminal.")
                st.rerun()

    # Update
    with st.expander("✏️ Update Criminal"):
        update_record("criminals", "criminal_id", role)

    # Delete
    if role == "Admin":
        delete_record("criminals", "criminal_id", "first_name", "last_name", "crime_involvement", "criminal_id")


def manage_crimes(role):
    st.subheader("Manage Crimes")
    data = load_data("crimes")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add Crime"):
        with st.form("add_crime", clear_on_submit=True):
            t = st.text_input("Type")
            desc = st.text_area("Description")
            date = st.date_input("Date Committed", datetime.now().date())
            loc = st.text_input("Location")
            if st.form_submit_button("Add"):
                execute_query("INSERT INTO crimes (type,description,date_committed,location) VALUES (%s,%s,%s,%s)",
                              (t, desc, date, loc))
                st.success("✅ Added crime.")
                st.rerun()

    with st.expander("✏️ Update Crime"):
        update_record("crimes", "crime_id", role)

    if role == "Admin":
        delete_record("crimes", "crime_id", "type")


def manage_cases(role):
    st.subheader("Manage Cases")
    data = load_data("cases")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add Case"):
        with st.form("add_case", clear_on_submit=True):
            crime_id = st.number_input("Crime ID", min_value=1)
            station_id = st.number_input("Station ID", min_value=1)
            court_id = st.number_input("Court ID", min_value=1)
            summary = st.text_area("Summary")
            status = st.selectbox("Status", ["Open", "Closed", "Under Investigation"])
            date_filed = st.date_input("Date Filed", datetime.now().date())
            if st.form_submit_button("Add"):
                execute_query(
                    "INSERT INTO cases (crime_id,station_id,court_id,summary,status,date_filed) VALUES (%s,%s,%s,%s,%s,%s)",
                    (crime_id, station_id, court_id, summary, status, date_filed)
                )
                st.success("✅ Added case.")
                st.rerun()

    with st.expander("✏️ Update Case"):
        update_record("cases", "case_id", role)

    if role == "Admin":
        delete_record("cases", "case_id", "summary")


def manage_officers(role):
    st.subheader("Manage Police Officers")
    data = load_data("police_officer")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add Officer"):
        with st.form("add_officer", clear_on_submit=True):
            sid = st.number_input("Station ID", min_value=1)
            first = st.text_input("First Name")
            last = st.text_input("Last Name")
            badge = st.text_input("Badge Number")
            rank = st.text_input("Rank")
            hire = st.date_input("Hire Date", datetime.now().date())
            if st.form_submit_button("Add"):
                execute_query(
                    "INSERT INTO police_officer (station_id,first_name,last_name,badge_number,officer_rank,hire_date) VALUES (%s,%s,%s,%s,%s,%s)",
                    (sid, first, last, badge, rank, hire)
                )
                st.success("✅ Added officer.")
                st.rerun()

    with st.expander("✏️ Update Officer"):
        update_record("police_officer", "officer_id", role)

    if role == "Admin":
        delete_record("police_officer", "officer_id", "first_name", "last_name")


def manage_victims(role):
    st.subheader("Manage Victims")
    data = load_data("victims")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add Victim"):
        with st.form("add_victim", clear_on_submit=True):
            first = st.text_input("First Name")
            last = st.text_input("Last Name")
            dob = st.date_input("DOB", datetime.now().date())
            addr = st.text_area("Address")
            phone = st.text_input("Phone")
            if st.form_submit_button("Add"):
                execute_query(
                    "INSERT INTO victims (first_name,last_name,dob,address,phone) VALUES (%s,%s,%s,%s,%s)",
                    (first, last, dob, addr, phone)
                )
                st.success("✅ Added victim.")
                st.rerun()

    with st.expander("✏️ Update Victim"):
        update_record("victims", "victim_id", role)

    if role == "Admin":
        delete_record("victims", "victim_id", "first_name", "last_name")


def manage_courts(role):
    st.subheader("Manage Courts")
    data = load_data("courts")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add Court"):
        with st.form("add_court", clear_on_submit=True):
            name = st.text_input("Court Name")
            ctype = st.selectbox("Type", ["District", "High", "Supreme", "Magistrate"])
            city = st.text_input("City")
            state = st.text_input("State")
            if st.form_submit_button("Add"):
                execute_query("INSERT INTO courts (name,type,city,state) VALUES (%s,%s,%s,%s)",
                              (name, ctype, city, state))
                st.success("✅ Added court.")
                st.rerun()

    with st.expander("✏️ Update Court"):
        update_record("courts", "court_id", role)

    if role == "Admin":
        delete_record("courts", "court_id", "name")


def manage_stations(role):
    st.subheader("Manage Police Stations")
    data = load_data("police_station")
    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add Station"):
        with st.form("add_station", clear_on_submit=True):
            name = st.text_input("Station Name")
            addr = st.text_area("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            if st.form_submit_button("Add"):
                execute_query("INSERT INTO police_station (name,address,city,state) VALUES (%s,%s,%s,%s)",
                              (name, addr, city, state))
                st.success("✅ Added station.")
                st.rerun()

    with st.expander("✏️ Update Station"):
        update_record("police_station", "station_id", role)

    if role == "Admin":
        delete_record("police_station", "station_id", "name")
