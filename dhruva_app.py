import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="D.H.R.U.V.A.", page_icon="🦅", layout="wide")

# --- DATABASE CONNECTION ---
try:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Connection Error: {e}")

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["HOME", "ABOUT", "INVESTIGATIONS", "REPORT", "CONTACT"])

# --- TAB 3: INVESTIGATIONS (Matches your Sheet) ---
with tab3:
    if conn:
        try:
            df_inv = conn.read(worksheet="Investigations", ttl=0)
            if not df_inv.empty:
                for _, row in df_inv.iterrows():
                    st.markdown(f"### {row['Title']}")
                    st.write(f"**Verdict:** {row['Verdict']} | **Date:** {row['Date']}")
                    st.write(row['Details'])
                    st.divider()
        except: st.info("No declassified files found.")

# --- TAB 4: REPORT MYSTERY (Matched to your Screenshot Headers) ---
with tab4:
    st.subheader("TRANSMIT ANOMALY DATA")
    with st.form("anomaly_form", clear_on_submit=True):
        name = st.text_input("FULL NAME *")
        phone = st.text_input("CONTACT NO *")
        loc = st.text_input("LOCATION *")
        cat = st.selectbox("CATEGORY", ["Haunting", "UFO", "Other"])
        desc = st.text_area("DETAILED DESCRIPTION *")
        
        if st.form_submit_button("SUBMIT"):
            if name and desc and conn:
                # THESE KEYS MUST MATCH YOUR SHEET HEADERS EXACTLY
                new_data = pd.DataFrame([{
                    "Timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "FULL_NAME": name,
                    "CONTACT_NUM": phone,
                    "LOCATION": loc,
                    "CATEGORY": cat,
                    "DETAILED DESCRIPTION": desc
                }])
                try:
                    existing = conn.read(worksheet="Reports", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Reports", data=updated)
                    st.success("INTEL SAVED PERMANENTLY.")
                except Exception as e:
                    st.error(f"Database Error: {e}")

# --- TAB 5: CONTACT (Matched to your Screenshot Headers) ---
with tab5:
    with st.form("contact_form", clear_on_submit=True):
        cn = st.text_input("FULL NAME")
        num = st.text_input("NUMBER")
        ce = st.text_input("EMAIL")
        cm = st.text_area("MESSAGE")
        
        if st.form_submit_button("SEND"):
            if ce and cm and conn:
                new_msg = pd.DataFrame([{
                    "Timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "FULL_NAME": cn,
                    "Number": num,
                    "EMAIL": ce,
                    "MESSAGE": cm
                }])
                try:
                    existing_m = conn.read(worksheet="Messages", ttl=0)
                    updated_m = pd.concat([existing_m, new_msg], ignore_index=True)
                    conn.update(worksheet="Messages", data=updated_m)
                    st.success("MESSAGE SENT.")
                except Exception as e:
                    st.error(f"Error: {e}")
