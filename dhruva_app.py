import streamlit as st
import pandas as pd
import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="D.H.R.U.V.A. | National Anomaly Research",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DATABASE CONNECTION ---
conn = None
try:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"DATABASE OFFLINE: {e}")

# --- SESSION STATE FOR TEAM ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'team_data' not in st.session_state:
    st.session_state['team_data'] = {
        "m1": {"name": "Field Agent Alpha", "info": "Specialist in EMF and EVPs."},
        "m2": {"name": "Field Agent Beta", "info": "Specialist in Thermal Imaging."},
        "m3": {"name": "Field Agent Gamma", "info": "Specialist in Historical Research."}
    }

access_code = st.query_params.to_dict().get("access")

# --- 2. PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Raleway:wght@300;400&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Raleway', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0A0A0A; border-bottom: 1px solid #111; justify-content: center; }
    .stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
    .ips-title { font-family: 'Cinzel', serif; font-size: 55px; text-align: center; letter-spacing: 5px; }
    .ips-motto { text-align: center; color: #00D4FF; font-style: italic; font-weight: bold; margin-bottom: 30px; }
    .ips-block { background-color: #0A0A0A; border-left: 3px solid #00D4FF; padding: 30px; margin: 20px 0; }
    .team-card { background-color: #0A0A0A; border: 1px solid #1A1A1A; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 10px; }
    .stButton > button { background-color: #7B0000 !important; color: white; border-radius: 0; width: 100%; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("<div class='ips-title'>D.H.R.U.V.A.</div>", unsafe_allow_html=True)
st.markdown("<div class='ips-motto'>\"Fear is just missing data. Logic is the cure.\"</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["HOME", "ABOUT US", "INVESTIGATIONS", "REPORT MYSTERY", "CONTACT"])

with tab2:
    st.markdown("<h2 style='font-family:Cinzel;'>THE DIRECTORATE</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1: 
        try: st.image("director.png", width=300)
        except: st.info("Pranav Anil Rahane")
    with c2:
        st.markdown("<h3 style='color:#00D4FF;'>Pranav Anil Rahane</h3>", unsafe_allow_html=True)
        st.write("Founder & Chief Investigator | CSE (AI & DS), IIIT Kottayam")
        st.write("D.H.R.U.V.A. (Digital Holistic Residual Unexplained Variable Analysis) is a youth-led unit bridging folklore and modern science.")

    st.markdown("---")
    st.markdown("<h2 style='font-family:Cinzel; text-align:center;'>THE FIELD TEAM</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    cols = [t1, t2, t3]
    for i, col in enumerate(cols):
        with col:
            try: st.image(f"member{i+1}.png")
            except: st.markdown("<div class='team-card'>👤 MEMBER SLOT</div>", unsafe_allow_html=True)
            m_key = f"m{i+1}"
            st.markdown(f"**{st.session_state['team_data'][m_key]['name']}**")
            st.caption(st.session_state['team_data'][m_key]['info'])

with tab4:
    with st.form("anomaly_form", clear_on_submit=True):
        fn = st.text_input("FULL NAME *"); ph = st.text_input("CONTACT NO *")
        lc = st.text_input("LOCATION *"); ct = st.selectbox("CATEGORY", ["Haunting", "UFO", "Other"])
        ds = st.text_area("DETAILED DESCRIPTION *")
        if st.form_submit_button("TRANSMIT INTEL"):
            if fn and ds and conn:
                new_row = pd.DataFrame([{"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "FULL_NAME": fn, "CONTACT_NUM": ph, "LOCATION": lc, "CATEGORY": ct, "DETAILED DESCRIPTION": ds}])
                try:
                    ex = conn.read(worksheet="Reports", ttl=0)
                    up = pd.concat([ex, new_row], ignore_index=True)
                    conn.update(worksheet="Reports", data=up)
                    st.success("INTEL RECEIVED.")
                except Exception as e: st.error(f"Error: {e}")

with tab5:
    with st.form("contact_form", clear_on_submit=True):
        st.markdown("<h3 style='font-family:Cinzel;'>DIRECT CONTACT</h3>", unsafe_allow_html=True)
        cn = st.text_input("NAME *"); n = st.text_input("Number"); ce = st.text_input("EMAIL *"); cm = st.text_area("MESSAGE *")
        if st.form_submit_button("SEND"):
            if ce and cm and conn:
                new_m = pd.DataFrame([{"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "FULL_NAME": cn, "Number": n, "EMAIL": ce, "MESSAGE": cm}])
                try:
                    ex = conn.read(worksheet="Messages", ttl=0)
                    up = pd.concat([ex, new_m], ignore_index=True)
                    conn.update(worksheet="Messages", data=up)
                    st.success("MESSAGE SENT.")
                except Exception as e: st.error(f"Error: {e}")

# --- 5. HIDDEN HQ CONTROL ---
if access_code == "classified":
    with st.sidebar:
        st.markdown("### 🔐 HQ CONTROL")
        if not st.session_state['auth']:
            u = st.text_input("ID"); p = st.text_input("KEY", type="password")
            if st.button("LOGIN"):
                if u == "Pranav" and p == "DhruvaBot": st.session_state['auth'] = True; st.rerun()
        
        if st.session_state['auth']:
            st.success("DIRECTOR ONLINE")
            
            # --- MESSAGE SECTION ---
            with st.expander("✉️ READ MESSAGES"):
                try:
                    msgs = conn.read(worksheet="Messages", ttl=0)
                    st.dataframe(msgs)
                except: st.error("Could not fetch messages.")

            # --- TEAM MANAGEMENT ---
            with st.expander("👥 MANAGE FIELD TEAM"):
                for i in range(1, 4):
                    st.markdown(f"**Member {i} Settings**")
                    m_key = f"m{i}"
                    st.session_state['team_data'][m_key]['name'] = st.text_input(f"Name {i}", st.session_state['team_data'][m_key]['name'])
                    st.session_state['team_data'][m_key]['info'] = st.text_area(f"Info {i}", st.session_state['team_data'][m_key]['info'])
                    st.info(f"Upload 'member{i}.png' to GitHub to show image.")
                st.success("Team Info Live-Updated Below.")

            if st.checkbox("📥 VIEW ANOMALY REPORTS"):
                st.dataframe(conn.read(worksheet="Reports", ttl=0))
            
            if st.button("LOGOUT"): st.session_state['auth'] = False; st.rerun()

st.markdown("<div style='text-align:center; color:#333; font-size:12px; padding:40px;'>© 2026 D.H.R.U.V.A. | LOGIC OVER FEAR</div>", unsafe_allow_html=True)
