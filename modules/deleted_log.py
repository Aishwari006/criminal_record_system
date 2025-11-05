import streamlit as st
import pandas as pd
import json
from db.connection import get_db_connection, execute_query


def deleted_log_page(role):
    st.header("🗑️ Deleted Records Log")

    # Fetch deleted data
    data = execute_query("SELECT * FROM deleted_records_log ORDER BY deleted_at DESC", fetch_all=True)
    if not data:
        st.info("No deleted records found yet.")
        return

    df = pd.DataFrame(data)

    # Parse JSON field into separate columns
    parsed_rows = []
    for _, row in df.iterrows():
        try:
            record_data = json.loads(row["record_data"])
            record_data_flat = {
                "log_id": row["log_id"],
                "table_name": row["table_name"],
                **record_data,
                "deleted_at": row["deleted_at"],
            }
            parsed_rows.append(record_data_flat)
        except Exception:
            parsed_rows.append({
                "log_id": row["log_id"],
                "table_name": row["table_name"],
                "record_data": row["record_data"],
                "deleted_at": row["deleted_at"],
            })

    parsed_df = pd.DataFrame(parsed_rows)

    # 🔹 Smart column ordering
    preferred_order = [
        "log_id", "table_name", "first_name", "last_name",
        "type", "crime_type", "summary", "city", "state", "status",
        "dob", "address", "location", "badge_number", "officer_rank",
        "station_id", "court_id", "crime_id", "deleted_at"
    ]
    existing_cols = [c for c in preferred_order if c in parsed_df.columns]
    other_cols = [c for c in parsed_df.columns if c not in existing_cols]
    final_cols = existing_cols + other_cols

    parsed_df = parsed_df[final_cols]

    # Title-case table names for readability
    parsed_df["table_name"] = parsed_df["table_name"].str.replace("_", " ").str.title()

    st.dataframe(parsed_df, use_container_width=True)

    # --- RESTORE SECTION (Admin only) ---
    if role == "Admin":
        st.subheader("♻️ Restore Deleted Records (Admin Only)")

        if len(parsed_df) > 0:
            selected_row = st.selectbox(
                "Select a record to restore:",
                parsed_df.apply(
                    lambda r: f"{r['log_id']} - {r['table_name']} ({r.get('first_name', '')} {r.get('last_name', '')})",
                    axis=1
                )
            )

            if selected_row:
                log_id = int(selected_row.split(" - ")[0])
                table_name = selected_row.split(" - ")[1].split(" ")[0].lower()

                if st.button("♻️ Restore Selected Record", type="primary"):
                    try:
                        # Map plural table names → correct singular procedure names
                        restore_map = {
                            "criminals": "sp_restore_criminal",
                            "crimes": "sp_restore_crime",
                            "cases": "sp_restore_case",
                            "victims": "sp_restore_victim",
                            "police_officer": "sp_restore_officer",
                            "police_station": "sp_restore_station",
                            "courts": "sp_restore_court"
                        }

                        proc_name = restore_map.get(table_name.lower())
                        if not proc_name:
                            st.error(f"No restore procedure found for table `{table_name}`.")
                            return

                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.callproc(proc_name, [log_id])
                        conn.commit()
                        cursor.close()
                        conn.close()

                        st.success(f"✅ Restored record from `{table_name}` successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Restore failed: {e}")

    else:
        # Officers or others can only view deleted logs
        st.info("🔒 Restore option is restricted to Admin users only.")
