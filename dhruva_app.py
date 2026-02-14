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

# --- SESSION STATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'team' not in st.session_state:
    st.session_state['team'] = {
        "m1": {"name": "Slot 01", "bio": "Awaiting Personnel..."},
        "m2": {"name": "Slot 02", "bio": "Awaiting Personnel..."},
        "m3": {"name": "Slot 03", "bio": "Awaiting Personnel..."}
    }

access_code = st.query_params.to_dict().get("access")

# --- 2. CSS STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Raleway:wght@300;400&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Raleway', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0A0A0A; justify-content: center; }
    .stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
    .ips-title { font-family: 'Cinzel', serif; font-size: 55px; text-align: center; letter-spacing: 5px; margin-bottom: 0; }
    .ips-motto { text-align: center; color: #00D4FF; font-style: italic; font-weight: bold; margin-bottom: 30px; }
    .ips-block { background-color: #0A0A0A; border-left: 3px solid #00D4FF; padding: 30px; margin: 20px 0; }
    .team-card { background-color: #0A0A0A; border: 1px solid #1A1A1A; padding: 20px; text-align: center; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER & LOGO ---
col_h1, col_h2, col_h3 = st.columns([1, 4, 1])
with col_h2:
    try: st.image("logo.png", width=150)
    except: st.markdown("<h1 style='text-align:center;'>🦅</h1>", unsafe_allow_html=True)
    st.markdown("<div class='ips-title'>D.H.R.U.V.A.</div>", unsafe_allow_html=True)
    st.markdown("<div class='ips-motto'>\"Fear is just missing data. Logic is the cure.\"</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["HOME", "ABOUT US", "INVESTIGATIONS", "REPORT MYSTERY", "CONTACT"])

with tab1:
    col_i1, col_i2 = st.columns([1, 2])
    with col_i1:
        try: st.image("gaurav_tiwari.png", use_container_width=True)
        except: st.info("Late Rev. Gaurav Tiwari")
    with col_i2:
        st.markdown("<div class='ips-block'><h3>OUR INSPIRATION</h3><p>\"Ghosts or consciousness survive physical death.\"</p><b>- Late Rev. Gaurav Tiwari</b></div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 style='font-family:Cinzel;'>THE DIRECTORATE</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1: 
        try: st.image("director.png", width=300)
        except: st.info("Pranav Anil Rahane")
    with c2:
        st.markdown("<h3 style='color:#00D4FF;'>Pranav Anil Rahane</h3>", unsafe_allow_html=True)
        st.write("Founder & Chief Investigator | CSE (AI & DS), IIIT Kottayam")
    
    st.markdown("---")
    st.markdown("<h2 style='font-family:Cinzel; text-align:center;'>FIELD TEAM</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    for i, col in enumerate([t1, t2, t3]):
        with col:
            try: st.image(f"member{i+1}.png")
            except: st.markdown("<div class='team-card'>👤 Awaiting Data</div>", unsafe_allow_html=True)
            m = st.session_state['team'][f"m{i+1}"]
            st.markdown(f"**{m['name']}**")
            st.caption(m['bio'])

with tab3:
    st.markdown("<h2 style='font-family:Cinzel;'>INVESTIGATION ARCHIVES</h2>", unsafe_allow_html=True)
    st.info("⚠️ SCANNING FOR DECLASSIFIED INTEL...")
    st.write("D.H.R.U.V.A. is currently in the initial phase of operation. We are analyzing multiple residual variables across active sites.")
    if conn:
        try:
            df = conn.read(worksheet="Investigations", ttl=0)
            if not df.empty:
                for _, row in df.iterrows():
                    st.markdown(f"<div class='ips-block'><h4>{row['Title']}</h4><p>{row['Details']}</p><b>{row['Verdict']}</b></div>", unsafe_allow_html=True)
        except: pass

with tab4:
    with st.form("report_form", clear_on_submit=True):
        st.markdown("<h3 style='font-family:Cinzel;'>TRANSMIT ANOMALY DATA</h3>", unsafe_allow_html=True)
        fn = st.text_input("FULL NAME *"); ph = st.text_input("CONTACT NO *")
        lc = st.text_input("LOCATION *"); ct = st.selectbox("CATEGORY", ["Haunting", "UFO", "Other"])
        ds = st.text_area("DETAILED DESCRIPTION *")
        if st.form_submit_button("TRANSMIT"):
            if fn and ds and conn:
                new_row = pd.DataFrame([{"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "FULL_NAME": fn, "CONTACT_NUM": ph, "LOCATION": lc, "CATEGORY": ct, "DETAILED DESCRIPTION": ds}])
                try:
                    ex = conn.read(worksheet="Reports", ttl=0); up = pd.concat([ex, new_row], ignore_index=True); conn.update(worksheet="Reports", data=up)
                    st.success("INTEL RECEIVED.")
                except Exception as e: st.error(f"Sync Failed: {e}")

with tab5:
    st.markdown('<div style="background-color:#0A0A0A; border:1px solid #1A1A1A; padding:30px; text-align:center;"><a href="mailto:team.dhruva.research@gmail.com" style="color:#2ECC71; font-weight:bold; font-size:20px; text-decoration:none;">✉️ team.dhruva.research@gmail.com</a></div>', unsafe_allow_html=True)
    with st.form("contact"):
        st.markdown("<h3 style='font-family:Cinzel;'>DIRECT CONTACT</h3>", unsafe_allow_html=True)
        cn = st.text_input("NAME *"); ce = st.text_input("EMAIL *"); cm = st.text_area("MESSAGE *")
        if st.form_submit_button("SEND"):
            if ce and cm and conn:
                new_m = pd.DataFrame([{"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "FULL_NAME": cn, "EMAIL": ce, "MESSAGE": cm}])
                try:
                    ex = conn.read(worksheet="Messages", ttl=0); up = pd.concat([ex, new_m], ignore_index=True); conn.update(worksheet="Messages", data=up)
                    st.success("TRANSMITTED.")
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
            with st.expander("✉️ READ MESSAGES"):
                try: st.dataframe(conn.read(worksheet="Messages", ttl=0))
                except: st.error("No data found.")
            with st.expander("👥 TEAM MANAGEMENT"):
                for i in range(1, 4):
                    mk = f"m{i}"
                    st.session_state['team'][mk]['name'] = st.text_input(f"Member {i} Name", st.session_state['team'][mk]['name'])
                    st.session_state['team'][mk]['bio'] = st.text_area(f"Member {i} Info Pad", st.session_state['team'][mk]['bio'])
            if st.button("LOGOUT"): st.session_state['auth'] = False; st.rerun()

st.markdown("<div style='text-align:center; color:#333; font-size:12px; padding:40px;'>© 2026 D.H.R.U.V.A. | LOGIC OVER FEAR</div>", unsafe_allow_html=True)
