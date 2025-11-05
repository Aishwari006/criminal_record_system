import streamlit as st
import pandas as pd
from db.connection import execute_query
from utils.helpers import get_full_dropdown_data


def linking_crud_page(role):
    st.header("Manage Record Links (Many-to-Many)")

    table_to_manage = st.selectbox(
        "Select Link Type",
        [
            "Criminals <-> Crimes",
            "Crimes <-> Victims",
            "Cases <-> Officers",
            "Police Stations <-> Cases",
            "Cases <-> Courts",
            "Crimes <-> Cases",
            "Police Stations <-> Officers"
        ]
    )

    if table_to_manage == "Criminals <-> Crimes":
        manage_crime_involvement(role)
    elif table_to_manage == "Crimes <-> Victims":
        manage_crime_victims(role)
    elif table_to_manage == "Cases <-> Officers":
        manage_case_assignment(role)
    elif table_to_manage == "Police Stations <-> Cases":
        manage_registrations(role)
    elif table_to_manage == "Cases <-> Courts":
        manage_case_trial(role)
    elif table_to_manage == "Crimes <-> Cases":
        manage_case_crimes(role)
    elif table_to_manage == "Police Stations <-> Officers":
        manage_employees(role)


# -------------------- Criminals ↔ Crimes --------------------
def manage_crime_involvement(role):
    st.subheader("Link Criminals to Crimes")

    data = execute_query("""
        SELECT ci.involvement_id,
               CONCAT(cr.first_name, ' ', cr.last_name) AS criminal_name,
               c.type AS crime_type,
               ci.role
        FROM crime_involvement ci
        JOIN criminals cr ON ci.criminal_id = cr.criminal_id
        JOIN crimes c ON ci.crime_id = c.crime_id
    """, fetch_all=True)

    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add New Link"):
        criminal_map = get_full_dropdown_data(
            "SELECT criminal_id, CONCAT(first_name, ' ', last_name) AS name FROM criminals ORDER BY first_name",
            "criminal_id", "name"
        )
        crime_map = get_full_dropdown_data(
            "SELECT crime_id, type AS name FROM crimes ORDER BY type",
            "crime_id", "name"
        )

        with st.form("link_criminal_crime"):
            criminal_name = st.selectbox("Criminal", list(criminal_map.keys()))
            crime_name = st.selectbox("Crime", list(crime_map.keys()))
            role_in_crime = st.selectbox("Role", ["Suspect", "Convicted", "Accomplice", "Witness"])
            if st.form_submit_button("Add Link"):
                execute_query(
                    "INSERT INTO crime_involvement (criminal_id, crime_id, role) VALUES (%s, %s, %s)",
                    (criminal_map[criminal_name], crime_map[crime_name], role_in_crime)
                )
                st.success("Criminal linked successfully!")
                st.rerun()

    if role == "Admin" and data:
        with st.expander("🗑️ Delete Criminal–Crime Link (Admin Only)"):
            link_map = {
                f"{d['criminal_name']} ↔ {d['crime_type']} ({d['role']}) (ID: {d['involvement_id']})": d['involvement_id']
                for d in data
            }
            selected = st.selectbox("Select Link to Delete", list(link_map.keys()))
            if st.checkbox("Confirm Deletion"):
                if st.button("Delete Link", type="primary"):
                    execute_query("DELETE FROM crime_involvement WHERE involvement_id=%s", (link_map[selected],))
                    st.success(f"Deleted link: {selected}")
                    st.rerun()


# -------------------- Crimes ↔ Victims --------------------
def manage_crime_victims(role):
    st.subheader("Link Victims to Crimes")

    data = execute_query("""
        SELECT cv.crime_victim_id,
               CONCAT(v.first_name, ' ', v.last_name) AS victim_name,
               c.type AS crime_type
        FROM crime_victims cv
        JOIN victims v ON cv.victim_id = v.victim_id
        JOIN crimes c ON cv.crime_id = c.crime_id
    """, fetch_all=True)

    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add New Link"):
        victim_map = get_full_dropdown_data(
            "SELECT victim_id, CONCAT(first_name, ' ', last_name) AS name FROM victims ORDER BY first_name",
            "victim_id", "name"
        )
        crime_map = get_full_dropdown_data(
            "SELECT crime_id, type AS name FROM crimes ORDER BY type",
            "crime_id", "name"
        )

        with st.form("link_victim_crime"):
            victim_name = st.selectbox("Victim", list(victim_map.keys()))
            crime_name = st.selectbox("Crime", list(crime_map.keys()))
            if st.form_submit_button("Add Link"):
                execute_query(
                    "INSERT INTO crime_victims (victim_id, crime_id) VALUES (%s, %s)",
                    (victim_map[victim_name], crime_map[crime_name])
                )
                st.success("Victim linked successfully!")
                st.rerun()

    if role == "Admin" and data:
        with st.expander("🗑️ Delete Victim–Crime Link (Admin Only)"):
            link_map = {
                f"{d['victim_name']} ↔ {d['crime_type']} (ID: {d['crime_victim_id']})": d['crime_victim_id']
                for d in data
            }
            selected = st.selectbox("Select Link to Delete", list(link_map.keys()))
            if st.checkbox("Confirm Deletion"):
                if st.button("Delete Link", type="primary"):
                    execute_query("DELETE FROM crime_victims WHERE crime_victim_id=%s", (link_map[selected],))
                    st.success(f"Deleted link: {selected}")
                    st.rerun()


# -------------------- Cases ↔ Officers --------------------
def manage_case_assignment(role):
    st.subheader("Assign Officers to Cases")

    data = execute_query("""
        SELECT ca.assignment_id,
               CONCAT(po.first_name, ' ', po.last_name, ' (', po.badge_number, ')') AS officer_name,
               c.summary AS case_summary,
               ca.role
        FROM case_assignment ca
        JOIN police_officer po ON ca.officer_id = po.officer_id
        JOIN cases c ON ca.case_id = c.case_id
    """, fetch_all=True)

    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add New Assignment"):
        case_map = get_full_dropdown_data(
            "SELECT case_id, CONCAT('Case #', case_id, ': ', SUBSTRING(summary, 1, 40)) AS name FROM cases ORDER BY case_id DESC",
            "case_id", "name"
        )
        officer_map = get_full_dropdown_data(
            "SELECT officer_id, CONCAT(first_name, ' ', last_name, ' (', badge_number, ')') AS name FROM police_officer ORDER BY first_name",
            "officer_id", "name"
        )

        with st.form("link_case_officer"):
            case_name = st.selectbox("Case", list(case_map.keys()))
            officer_name = st.selectbox("Officer", list(officer_map.keys()))
            role_in_case = st.selectbox("Role", ["Lead", "Support", "Investigator"])
            if st.form_submit_button("Assign Officer"):
                execute_query(
                    "INSERT INTO case_assignment (case_id, officer_id, role) VALUES (%s, %s, %s)",
                    (case_map[case_name], officer_map[officer_name], role_in_case)
                )
                st.success("Officer assigned successfully!")
                st.rerun()

    if role == "Admin" and data:
        with st.expander("🗑️ Delete Officer–Case Assignment (Admin Only)"):
            link_map = {
                f"{d['officer_name']} ↔ Case: {d['case_summary'][:30]} ({d['role']}) (ID: {d['assignment_id']})": d['assignment_id']
                for d in data
            }
            selected = st.selectbox("Select Assignment to Delete", list(link_map.keys()))
            if st.checkbox("Confirm Deletion"):
                if st.button("Delete Assignment", type="primary"):
                    execute_query("DELETE FROM case_assignment WHERE assignment_id=%s", (link_map[selected],))
                    st.success(f"Deleted assignment: {selected}")
                    st.rerun()


# -------------------- Police Stations ↔ Cases --------------------
def manage_registrations(role):
    st.subheader("Link Police Stations to Cases (Registrations)")

    data = execute_query("""
        SELECT r.registration_id, ps.name AS station_name, c.case_id, c.summary, r.registration_date
        FROM registrations r
        JOIN police_station ps ON r.station_id = ps.station_id
        JOIN cases c ON r.case_id = c.case_id
    """, fetch_all=True)

    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add New Registration"):
        station_map = get_full_dropdown_data("SELECT station_id, name FROM police_station ORDER BY name", "station_id", "name")
        case_map = get_full_dropdown_data("SELECT case_id, summary AS name FROM cases ORDER BY case_id DESC", "case_id", "name")

        with st.form("reg_form"):
            station = st.selectbox("Police Station", list(station_map.keys()))
            case = st.selectbox("Case", list(case_map.keys()))
            date = st.date_input("Registration Date")
            if st.form_submit_button("Add Link"):
                execute_query("INSERT INTO registrations (station_id, case_id, registration_date) VALUES (%s, %s, %s)",
                              (station_map[station], case_map[case], date))
                st.success("Registration added successfully!")
                st.rerun()

    if role == "Admin" and data:
        with st.expander("🗑️ Delete Registration Link (Admin Only)"):
            link_map = {
                f"{d['station_name']} ↔ Case #{d['case_id']} ({d['summary'][:30]}...)": d['registration_id']
                for d in data
            }
            selected = st.selectbox("Select Registration to Delete", list(link_map.keys()))
            if st.checkbox("Confirm Deletion"):
                if st.button("Delete Registration", type="primary"):
                    execute_query("DELETE FROM registrations WHERE registration_id=%s", (link_map[selected],))
                    st.success(f"Deleted registration: {selected}")
                    st.rerun()


# -------------------- Cases ↔ Courts --------------------
def manage_case_trial(role):
    st.subheader("Link Cases to Courts (Case-Trial)")

    data = execute_query("""
        SELECT ct.trial_id, c.case_id, c.summary, co.name AS court_name, ct.hearing_date, ct.status
        FROM case_trial ct
        JOIN cases c ON ct.case_id = c.case_id
        JOIN courts co ON ct.court_id = co.court_id
    """, fetch_all=True)

    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add New Case-Trial"):
        case_map = get_full_dropdown_data("SELECT case_id, summary AS name FROM cases ORDER BY case_id", "case_id", "name")
        court_map = get_full_dropdown_data("SELECT court_id, name FROM courts ORDER BY name", "court_id", "name")

        with st.form("trial_form"):
            case = st.selectbox("Case", list(case_map.keys()))
            court = st.selectbox("Court", list(court_map.keys()))
            hearing_date = st.date_input("Hearing Date")
            status = st.selectbox("Trial Status", ["Scheduled", "Ongoing", "Closed"])
            if st.form_submit_button("Add Link"):
                execute_query("INSERT INTO case_trial (case_id, court_id, hearing_date, status) VALUES (%s, %s, %s, %s)",
                              (case_map[case], court_map[court], hearing_date, status))
                st.success("Case-Trial linked successfully!")
                st.rerun()

    if role == "Admin" and data:
        with st.expander("🗑️ Delete Case-Trial Link (Admin Only)"):
            link_map = {
                f"Case #{d['case_id']} ↔ {d['court_name']} ({d['status']})": d['trial_id']
                for d in data
            }
            selected = st.selectbox("Select Trial to Delete", list(link_map.keys()))
            if st.checkbox("Confirm Deletion"):
                if st.button("Delete Trial", type="primary"):
                    execute_query("DELETE FROM case_trial WHERE trial_id=%s", (link_map[selected],))
                    st.success(f"Deleted trial link: {selected}")
                    st.rerun()


# -------------------- Crimes ↔ Cases --------------------
def manage_case_crimes(role):
    st.subheader("Link Crimes to Cases (Case-Crimes)")

    data = execute_query("""
        SELECT cc.case_crime_id, c.case_id, c.summary, cr.type AS crime_type, cc.details
        FROM case_crimes cc
        JOIN cases c ON cc.case_id = c.case_id
        JOIN crimes cr ON cc.crime_id = cr.crime_id
    """, fetch_all=True)

    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add New Case-Crime Link"):
        case_map = get_full_dropdown_data("SELECT case_id, summary AS name FROM cases ORDER BY case_id", "case_id", "name")
        crime_map = get_full_dropdown_data("SELECT crime_id, type AS name FROM crimes ORDER BY type", "crime_id", "name")

        with st.form("case_crime_form"):
            case = st.selectbox("Case", list(case_map.keys()))
            crime = st.selectbox("Crime", list(crime_map.keys()))
            details = st.text_area("Details")
            if st.form_submit_button("Add Link"):
                execute_query("INSERT INTO case_crimes (case_id, crime_id, details) VALUES (%s, %s, %s)",
                              (case_map[case], crime_map[crime], details))
                st.success("Case-Crime linked successfully!")
                st.rerun()

    if role == "Admin" and data:
        with st.expander("🗑️ Delete Case-Crime Link (Admin Only)"):
            link_map = {
                f"Case #{d['case_id']} ↔ {d['crime_type']} ({d['details'][:20]}...)": d['case_crime_id']
                for d in data
            }
            selected = st.selectbox("Select Case-Crime to Delete", list(link_map.keys()))
            if st.checkbox("Confirm Deletion"):
                if st.button("Delete Case-Crime", type="primary"):
                    execute_query("DELETE FROM case_crimes WHERE case_crime_id=%s", (link_map[selected],))
                    st.success(f"Deleted case-crime: {selected}")
                    st.rerun()


# -------------------- Police Stations ↔ Officers --------------------
def manage_employees(role):
    st.subheader("Link Police Stations to Officers (Employees)")

    data = execute_query("""
        SELECT e.employee_id, ps.name AS station_name, CONCAT(po.first_name, ' ', po.last_name) AS officer_name, e.assigned_date
        FROM employees e
        JOIN police_station ps ON e.station_id = ps.station_id
        JOIN police_officer po ON e.officer_id = po.officer_id
    """, fetch_all=True)

    st.dataframe(pd.DataFrame(data) if data else pd.DataFrame())

    with st.expander("➕ Add New Employee Link"):
        station_map = get_full_dropdown_data("SELECT station_id, name FROM police_station ORDER BY name", "station_id", "name")
        officer_map = get_full_dropdown_data(
            "SELECT officer_id, CONCAT(first_name, ' ', last_name) AS name FROM police_officer ORDER BY first_name",
            "officer_id", "name"
        )

        with st.form("emp_form"):
            station = st.selectbox("Police Station", list(station_map.keys()))
            officer = st.selectbox("Officer", list(officer_map.keys()))
            date = st.date_input("Assigned Date")
            if st.form_submit_button("Add Link"):
                execute_query("INSERT INTO employees (station_id, officer_id, assigned_date) VALUES (%s, %s, %s)",
                              (station_map[station], officer_map[officer], date))
                st.success("Officer assigned successfully!")
                st.rerun()

    if role == "Admin" and data:
        with st.expander("🗑️ Delete Employee Link (Admin Only)"):
            link_map = {
                f"{d['station_name']} ↔ {d['officer_name']} ({d['assigned_date']})": d['employee_id']
                for d in data
            }
            selected = st.selectbox("Select Employee Link to Delete", list(link_map.keys()))
            if st.checkbox("Confirm Deletion"):
                if st.button("Delete Employee", type="primary"):
                    execute_query("DELETE FROM employees WHERE employee_id=%s", (link_map[selected],))
                    st.success(f"Deleted employee link: {selected}")
                    st.rerun()
