import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="D.H.R.U.V.A.", page_icon="🦅", layout="wide")

# Safe Connection
conn = None
try:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("SYSTEM ERROR: Library not found. Please reboot app after adding st-gsheets-connection to requirements.txt")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["HOME", "ABOUT", "INVESTIGATIONS", "REPORT", "CONTACT"])

with tab4:
    with st.form("r_form", clear_on_submit=True):
        fn = st.text_input("FULL_NAME")
        ph = st.text_input("CONTACT_NUM")
        lc = st.text_input("LOCATION")
        cat = st.selectbox("CATEGORY", ["Haunting", "UFO", "Other"])
        ds = st.text_area("DETAILED DESCRIPTION")
        
        if st.form_submit_button("TRANSMIT"):
            if fn and ds and conn:
                new_row = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "FULL_NAME": fn,
                    "CONTACT_NUM": ph,
                    "LOCATION": lc,
                    "CATEGORY": cat,
                    "DETAILED DESCRIPTION": ds
                }])
                try:
                    df = conn.read(worksheet="Reports", ttl=0)
                    updated = pd.concat([df, new_row], ignore_index=True)
                    conn.update(worksheet="Reports", data=updated)
                    st.success("DATA SAVED TO HQ.")
                except Exception as e:
                    st.error(f"Save Failed: {e}")

with tab5:
    with st.form("c_form", clear_on_submit=True):
        cfn = st.text_input("FULL_NAME")
        cnum = st.text_input("Number")
        cem = st.text_input("EMAIL")
        cmsg = st.text_area("MESSAGE")
        if st.form_submit_button("SEND"):
            if cem and cmsg and conn:
                new_m = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "FULL_NAME": cfn,
                    "Number": cnum,
                    "EMAIL": cem,
                    "MESSAGE": cmsg
                }])
                try:
                    df_m = conn.read(worksheet="Messages", ttl=0)
                    updated_m = pd.concat([df_m, new_m], ignore_index=True)
                    conn.update(worksheet="Messages", data=updated_m)
                    st.success("MESSAGE SENT.")
                except Exception as e: st.error(f"Error: {e}")
