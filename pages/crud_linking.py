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
            "Cases <-> Officers"
        ]
    )

    if table_to_manage == "Criminals <-> Crimes":
        manage_crime_involvement(role)
    elif table_to_manage == "Crimes <-> Victims":
        manage_crime_victims(role)
    elif table_to_manage == "Cases <-> Officers":
        manage_case_assignment(role)


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

    # ---------- ADD ----------
    with st.expander("Add New Link"):
        criminal_map = get_full_dropdown_data(
            "SELECT criminal_id, CONCAT(first_name, ' ', last_name) AS name FROM criminals ORDER BY first_name",
            "criminal_id", "name"
        )
        crime_map = get_full_dropdown_data(
            "SELECT crime_id, type AS name FROM crimes ORDER BY type",
            "crime_id", "name"
        )

        with st.form(key="link_form_criminal_crime", clear_on_submit=True):
            criminal_name = st.selectbox("Criminal", list(criminal_map.keys()))
            crime_name = st.selectbox("Crime", list(crime_map.keys()))
            role_in_crime = st.selectbox("Role", ["Suspect", "Convicted", "Accomplice", "Witness"])
            submit_button = st.form_submit_button("Link")

            if submit_button:
                query = "INSERT INTO crime_involvement (criminal_id, crime_id, role) VALUES (%s, %s, %s)"
                execute_query(query, (criminal_map[criminal_name], crime_map[crime_name], role_in_crime))
                st.success("Criminal linked to crime successfully!")
                st.rerun()

    # ---------- DELETE (Admin only) ----------
    if role == "Admin" and data:
        with st.expander("🗑️ Delete Criminal–Crime Link (Admin Only)"):
            link_map = {
                f"{d['criminal_name']} ↔ {d['crime_type']} ({d['role']}) (ID: {d['involvement_id']})": d['involvement_id']
                for d in data
            }
            selected = st.selectbox("Select Link to Delete", list(link_map.keys()))
            confirm = st.checkbox("I confirm this deletion.")
            if st.button("Delete Link", type="primary"):
                if confirm:
                    execute_query("DELETE FROM crime_involvement WHERE involvement_id=%s", (link_map[selected],))
                    st.success(f"Deleted link: {selected}")
                    st.rerun()
                else:
                    st.warning("Please confirm before deleting.")


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

    # ---------- ADD ----------
    with st.expander("Add New Link"):
        victim_map = get_full_dropdown_data(
            "SELECT victim_id, CONCAT(first_name, ' ', last_name) AS name FROM victims ORDER BY first_name",
            "victim_id", "name"
        )
        crime_map = get_full_dropdown_data(
            "SELECT crime_id, type AS name FROM crimes ORDER BY type",
            "crime_id", "name"
        )

        with st.form(key="link_form_victim_crime", clear_on_submit=True):
            victim_name = st.selectbox("Victim", list(victim_map.keys()))
            crime_name = st.selectbox("Crime", list(crime_map.keys()))
            submit_button = st.form_submit_button("Link")

            if submit_button:
                query = "INSERT INTO crime_victims (victim_id, crime_id) VALUES (%s, %s)"
                execute_query(query, (victim_map[victim_name], crime_map[crime_name]))
                st.success("Victim linked to crime successfully!")
                st.rerun()

    # ---------- DELETE (Admin only) ----------
    if role == "Admin" and data:
        with st.expander("🗑️ Delete Victim–Crime Link (Admin Only)"):
            link_map = {
                f"{d['victim_name']} ↔ {d['crime_type']} (ID: {d['crime_victim_id']})": d['crime_victim_id']
                for d in data
            }
            selected = st.selectbox("Select Link to Delete", list(link_map.keys()))
            confirm = st.checkbox("I confirm this deletion.")
            if st.button("Delete Link", type="primary"):
                if confirm:
                    execute_query("DELETE FROM crime_victims WHERE crime_victim_id=%s", (link_map[selected],))
                    st.success(f"Deleted link: {selected}")
                    st.rerun()
                else:
                    st.warning("Please confirm before deleting.")


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

    # ---------- ADD ----------
    with st.expander("Add New Assignment"):
        case_map = get_full_dropdown_data(
            "SELECT case_id, CONCAT('Case #', case_id, ': ', SUBSTRING(summary, 1, 40)) AS name FROM cases ORDER BY case_id DESC",
            "case_id", "name"
        )
        officer_map = get_full_dropdown_data(
            "SELECT officer_id, CONCAT(first_name, ' ', last_name, ' (', badge_number, ')') AS name FROM police_officer ORDER BY first_name",
            "officer_id", "name"
        )

        with st.form(key="link_form_case_officer", clear_on_submit=True):
            case_name = st.selectbox("Case", list(case_map.keys()))
            officer_name = st.selectbox("Officer", list(officer_map.keys()))
            role_in_case = st.selectbox("Role", ["Lead", "Support", "Investigator"])
            submit_button = st.form_submit_button("Assign Officer")

            if submit_button:
                query = "INSERT INTO case_assignment (case_id, officer_id, role) VALUES (%s, %s, %s)"
                execute_query(query, (case_map[case_name], officer_map[officer_name], role_in_case))
                st.success("Officer assigned to case successfully!")
                st.rerun()

    # ---------- DELETE (Admin only) ----------
    if role == "Admin" and data:
        with st.expander("🗑️ Delete Officer–Case Assignment (Admin Only)"):
            link_map = {
                f"{d['officer_name']} ↔ Case: {d['case_summary'][:30]}... ({d['role']}) (ID: {d['assignment_id']})": d['assignment_id']
                for d in data
            }
            selected = st.selectbox("Select Assignment to Delete", list(link_map.keys()))
            confirm = st.checkbox("I confirm this deletion.")
            if st.button("Delete Assignment", type="primary"):
                if confirm:
                    execute_query("DELETE FROM case_assignment WHERE assignment_id=%s", (link_map[selected],))
                    st.success(f"Deleted assignment: {selected}")
                    st.rerun()
                else:
                    st.warning("Please confirm before deleting.")
