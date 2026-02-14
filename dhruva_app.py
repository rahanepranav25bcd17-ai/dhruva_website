import streamlit as st
import pandas as pd
import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="D.H.R.U.V.A.", page_icon="🦅", layout="wide")

# 2. DATABASE CONNECTION (SAFE INITIALIZATION)
conn = None
try:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Connection Error: {e}")

# 3. TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["HOME", "ABOUT", "INVESTIGATIONS", "REPORT MYSTERY", "CONTACT"])

with tab3:
    st.markdown("## DECLASSIFIED FILES")
    if conn:
        try:
            df_inv = conn.read(worksheet="Investigations", ttl=0)
            for _, row in df_inv.iterrows():
                st.markdown(f"**{row['Title']}** ({row['Date']})")
                st.write(row['Details'])
                st.caption(f"VERDICT: {row['Verdict']}")
                st.divider()
        except: st.info("No cases currently listed.")

with tab4:
    st.markdown("## TRANSMIT ANOMALY DATA")
    with st.form("anomaly_form", clear_on_submit=True):
        fn = st.text_input("FULL NAME *")
        ph = st.text_input("CONTACT NO *")
        lc = st.text_input("LOCATION *")
        ct = st.selectbox("CATEGORY", ["Haunting", "UFO", "Other"])
        ds = st.text_area("DETAILED DESCRIPTION *")
        
        if st.form_submit_button("SUBMIT INTEL"):
            if fn and ds and conn:
                new_row = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "FULL_NAME": fn,
                    "CONTACT_NUM": ph,
                    "LOCATION": lc,
                    "CATEGORY": ct,
                    "DETAILED DESCRIPTION": ds
                }])
                try:
                    old_data = conn.read(worksheet="Reports", ttl=0)
                    updated = pd.concat([old_data, new_row], ignore_index=True)
                    conn.update(worksheet="Reports", data=updated)
                    st.success("INTEL RECEIVED PERMANENTLY.")
                except Exception as e: st.error(f"Sync Error: {e}")

with tab5:
    st.markdown("## CONTACT HQ")
    with st.form("contact_form", clear_on_submit=True):
        cfn = st.text_input("FULL NAME")
        cnu = st.text_input("NUMBER")
        cem = st.text_input("EMAIL")
        cms = st.text_area("MESSAGE")
        if st.form_submit_button("SEND MESSAGE"):
            if cem and cms and conn:
                new_msg = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "FULL_NAME": cfn,
                    "Number": cnu,
                    "EMAIL": cem,
                    "MESSAGE": cms
                }])
                try:
                    old_msg = conn.read(worksheet="Messages", ttl=0)
                    updated_msg = pd.concat([old_msg, new_msg], ignore_index=True)
                    conn.update(worksheet="Messages", data=updated_msg)
                    st.success("MESSAGE TRANSMITTED.")
                except Exception as e: st.error(f"Sync Error: {e}")
