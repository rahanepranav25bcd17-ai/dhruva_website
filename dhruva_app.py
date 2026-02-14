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

# --- AUTH & SESSION STATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'mission_text' not in st.session_state: 
    st.session_state['mission_text'] = "D.H.R.U.V.A. (Digital Holistic Residual Unexplained Variable Analysis) is a youth-led unit bridging folklore and modern science."

access_code = st.query_params.to_dict().get("access")

# --- 2. PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Raleway:wght@300;400&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Raleway', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0A0A0A; border-bottom: 1px solid #111; justify-content: center; }
    .stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
    .ips-title { font-family: 'Cinzel', serif; font-size: 55px; text-align: center; letter-spacing: 5px; margin-bottom: 0; }
    .ips-subtitle { font-family: 'Raleway', sans-serif; font-size: 14px; text-align: center; color: #00D4FF; letter-spacing: 4px; text-transform: uppercase; }
    .ips-motto { font-family: 'Raleway', sans-serif; font-size: 16px; text-align: center; color: #00D4FF; font-style: italic; font-weight: bold; margin-bottom: 30px; }
    .ips-block { background-color: #0A0A0A; border-left: 3px solid #00D4FF; padding: 30px; margin: 30px 0; border-radius: 0 10px 10px 0; }
    .green-box-container { background-color: #0A0A0A; border: 1px solid #1A1A1A; padding: 35px; max-width: 550px; margin: 20px auto; border-radius: 8px; text-align: center; }
    .stButton > button { background-color: #7B0000 !important; color: white; border-radius: 0; border: none; width: 100%; }
    .team-card { background-color: #0A0A0A; border: 1px solid #1A1A1A; padding: 20px; text-align: center; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
col_h1, col_h2, col_h3 = st.columns([1, 4, 1])
with col_h2:
    try: st.image("logo.png", width=150)
    except: st.markdown("<h1 style='text-align:center;'>🦅</h1>", unsafe_allow_html=True)
    st.markdown("<div class='ips-title'>D.H.R.U.V.A.</div>", unsafe_allow_html=True)
    st.markdown("<div class='ips-subtitle'>National Research & Anomaly Society</div>", unsafe_allow_html=True)
    st.markdown("<div class='ips-motto'>\"Fear is just missing data. Logic is the cure.\"</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["HOME", "ABOUT US", "INVESTIGATIONS", "REPORT MYSTERY", "CONTACT"])

with tab1:
    st.markdown("<h2 style='text-align:center; font-family:Cinzel;'>WE INVESTIGATE WHAT OTHERS FEAR</h2>", unsafe_allow_html=True)
    col_i1, col_i2 = st.columns([1, 2])
    with col_i1:
        try: st.image("gaurav_tiwari.png", use_container_width=True)
        except: st.info("Late Rev. Gaurav Tiwari")
    with col_i2:
        st.markdown(f"""
            <div class='ips-block'>
                <h3 style='color:#00D4FF !important; font-family:Cinzel;'>OUR INSPIRATION</h3>
                <p style='font-style:italic; font-size:18px; color:#DDD;'>"Ghosts or consciousness survive physical death."</p>
                <p style='color:#00D4FF; font-weight:bold; margin-bottom:0;'>- Late Rev. Gaurav Tiwari</p>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 style='font-family:Cinzel;'>THE DIRECTORATE</h2>", unsafe_allow_html=True)
    col_dir1, col_dir2 = st.columns([1, 2])
    with col_dir1:
        try: st.image("director.png", width=300)
        except: st.info("Pranav Anil Rahane")
    with col_dir2:
        st.markdown("<h3 style='color:#00D4FF !important;'>Pranav Anil Rahane</h3>", unsafe_allow_html=True)
        st.caption("Founder & Chief Investigator | CSE (AI & DS), IIIT Kottayam")
        st.write(st.session_state['mission_text'])

    st.markdown("---")
    st.markdown("<h2 style='font-family:Cinzel; text-align:center;'>THE FIELD TEAM</h2>", unsafe_allow_html=True)
    
    # Placeholder for Team Members
    team_col1, team_col2, team_col3 = st.columns(3)
    with team_col1:
        st.markdown("<div class='team-card'><h4>Teammate 1</h4><p style='color:#888;'>Specialist Role</p></div>", unsafe_allow_html=True)
    with team_col2:
        st.markdown("<div class='team-card'><h4>Teammate 2</h4><p style='color:#888;'>Specialist Role</p></div>", unsafe_allow_html=True)
    with team_col3:
        st.markdown("<div class='team-card'><h4>Teammate 3</h4><p style='color:#888;'>Specialist Role</p></div>", unsafe_allow_html=True)

with tab3:
    if conn:
        try:
            df_inv = conn.read(worksheet="Investigations", ttl=0)
            if not df_inv.empty:
                for _, row in df_inv.iterrows():
                    st.markdown(f"<div class='ips-block'><h4>{row['Title']}</h4><p>{row['Details']}</p><b>VERDICT: {row['Verdict']}</b></div>", unsafe_allow_html=True)
            else: st.info("No declassified files found.")
        except: st.info("Accessing secure archives...")

with tab4:
    with st.form("anomaly_form", clear_on_submit=True):
        st.markdown("<h3 style='font-family:Cinzel;'>TRANSMIT ANOMALY DATA</h3>", unsafe_allow_html=True)
        c_a, c_b = st.columns(2)
        with c_a: fn = st.text_input("FULL NAME *"); ph = st.text_input("CONTACT NO *")
        with c_b: lc = st.text_input("LOCATION *"); ct = st.selectbox("CATEGORY", ["Haunting", "UFO", "Other"])
        ds = st.text_area("DETAILED DESCRIPTION *")
        if st.form_submit_button("SUBMIT INTEL"):
            if fn and ds and conn:
                new_rep = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "FULL_NAME": fn, "CONTACT_NUM": ph, "LOCATION": lc, "CATEGORY": ct, "DETAILED DESCRIPTION": ds
                }])
                try:
                    ex = conn.read(worksheet="Reports", ttl=0)
                    up = pd.concat([ex, new_rep], ignore_index=True)
                    conn.update(worksheet="Reports", data=up)
                    st.success("INTEL RECEIVED.")
                except Exception as e: st.error(f"Transmission failed: {e}")

with tab5:
    st.markdown('<div class="green-box-container"><a href="mailto:team.dhruva.research@gmail.com" style="color:#2ECC71; font-weight:bold; font-size:20px; text-decoration:none;">✉️ team.dhruva.research@gmail.com</a></div>', unsafe_allow_html=True)
    with st.form("contact_form", clear_on_submit=True):
        st.markdown("<h3 style='font-family:Cinzel;'>DIRECT MESSAGE</h3>", unsafe_allow_html=True)
        cn = st.text_input("NAME *"); n = st.text_input("Number"); ce = st.text_input("EMAIL *"); cm = st.text_area("MESSAGE *")
        if st.form_submit_button("SEND"):
            if ce and cm and conn:
                new_msg = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "FULL_NAME": cn, "Number": n, "EMAIL": ce, "MESSAGE": cm
                }])
                try:
                    ex = conn.read(worksheet="Messages", ttl=0)
                    up = pd.concat([ex, new_msg], ignore_index=True)
                    conn.update(worksheet="Messages", data=up)
                    st.success("MESSAGE SENT.")
                except Exception as e: st.error(f"Error: {e}")

# --- 5. HQ CONTROL ---
if access_code == "classified":
    with st.sidebar:
        st.markdown("### 🔐 HQ CONTROL")
        if not st.session_state['auth']:
            u = st.text_input("ID"); p = st.text_input("KEY", type="password")
            if st.button("LOGIN"):
                if u == "Pranav" and p == "DhruvaBot": st.session_state['auth'] = True; st.rerun()
        if st.session_state['auth']:
            st.success("DIRECTOR ONLINE")
            
            with st.expander("🛠️ EDIT ABOUT US"):
                new_mission = st.text_area("Edit Mission Statement", st.session_state['mission_text'])
                if st.button("UPDATE BIO"):
                    st.session_state['mission_text'] = new_mission
                    st.success("Bio Updated.")

            if st.checkbox("📥 VIEW REPORTS"):
                st.dataframe(conn.read(worksheet="Reports", ttl=0))
            
            if st.button("LOGOUT"): st.session_state['auth'] = False; st.rerun()

st.markdown("<div style='text-align:center; color:#333; font-size:12px; padding:40px;'>© 2026 D.H.R.U.V.A. | LOGIC OVER FEAR</div>", unsafe_allow_html=True)
