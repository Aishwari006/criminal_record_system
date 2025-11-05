import streamlit as st
from modules.dashboard import dashboard_page
from modules.crud_core import core_crud_page
from modules.crud_linking import linking_crud_page
from modules.reports import reports_page
from modules.deleted_log import deleted_log_page

st.set_page_config(layout="wide", page_title="Criminal Record System")
st.title("🚓 Criminal Record Management System")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard",
    "CRUD: Core Records",
    "CRUD: Linking Records",
    "Reports & Search",
    "Deleted Records Log"
])

st.sidebar.divider()
role = st.sidebar.selectbox("Select Role", ["Admin", "Officer"])
st.sidebar.info(f"Logged in as: **{role}**")

if page == "Dashboard":
    dashboard_page()
elif page == "CRUD: Core Records":
    core_crud_page(role)
elif page == "CRUD: Linking Records":
    linking_crud_page(role)
elif page == "Reports & Search":
    reports_page()
elif page == "Deleted Records Log":
    deleted_log_page()

