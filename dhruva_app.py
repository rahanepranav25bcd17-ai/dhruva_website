import streamlit as st
import pandas as pd
import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="D.H.R.U.V.A.", page_icon="🦅")

# 2. CONNECTION (With detailed error reporting)
conn = None
try:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"SYSTEM ERROR: Library not found. Check requirements.txt. Details: {e}")

# 3. REPORTING FORM
st.title("REPORT ANOMALY")
with st.form("final_form", clear_on_submit=True):
    name = st.text_input("FULL_NAME")
    num = st.text_input("CONTACT_NUM")
    loc = st.text_input("LOCATION")
    cat = st.selectbox("CATEGORY", ["Haunting", "UFO", "Other"])
    desc = st.text_area("DETAILED DESCRIPTION")
    
    if st.form_submit_button("TRANSMIT"):
        if conn and name and desc:
            # Match your spreadsheet EXACTLY
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "FULL_NAME": name,
                "CONTACT_NUM": num,
                "LOCATION": loc,
                "CATEGORY": cat,
                "DETAILED DESCRIPTION": desc
            }])
            try:
                # Force fresh read
                existing = conn.read(worksheet="Reports", ttl=0)
                updated = pd.concat([existing, new_entry], ignore_index=True)
                conn.update(worksheet="Reports", data=updated)
                st.success("INTEL SAVED PERMANENTLY.")
            except Exception as e:
                st.error(f"DATABASE ERROR: {e}")
        else:
            st.warning("Please check connection and fill required fields.")
