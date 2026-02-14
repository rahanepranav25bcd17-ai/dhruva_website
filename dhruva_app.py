import streamlit as st
import pandas as pd
import datetime

# 1. PAGE CONFIG
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
access_code = st.query_params.to_dict().get("access")

# 2. PREMIUM CSS (Sky Blue + Dark Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Raleway:wght@300;400&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Raleway', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0A0A0A; border-bottom: 1px solid #111; justify-content: center; }
    .stTabs [data-baseweb="tab"] { color: #888 !important; font-weight: bold; font-size: 14px; letter-spacing: 1px;}
    .stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
    .ips-title { font-family: 'Cinzel', serif; font-size: 55px; text-align: center; letter-spacing: 5px; margin-bottom: 0; }
    .ips-subtitle { font-family: 'Raleway', sans-serif; font-size: 14px; text-align: center; letter-spacing: 4px; color: #00D4FF; text-transform: uppercase; margin-bottom: 5px; }
    .ips-motto { font-family: 'Raleway', sans-serif; font-size: 16px; text-align: center; color: #00D4FF; font-style: italic; font-weight: bold; margin-bottom: 30px; }
    .ips-block { background-color: #0A0A0A; border-left: 3px solid #00D4FF; padding: 30px; margin: 30px 0; border-radius: 0 10px 10px 0; }
    .green-box-container { background-color: #0A0A0A; border: 1px solid #1A1A1A; padding: 35px; max-width: 550px; margin: 20px auto; border-radius: 8px; text-align: center; }
    .email-text { color: #2ECC71 !important; font-weight: bold; font-size: 22px; font-family: 'Courier New', monospace; text-decoration: none; }
    .stButton > button { background-color: #7B0000 !important; color: white; border-radius: 0; border: none; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 3. HEADER
col_h1, col_h2, col_h3 = st.columns([1, 4, 1])
with col_h2:
    try: st.image("logo.png", width=150)
    except: st.markdown("<h1 style='text-align:center;'>🦅</h1>", unsafe_allow_html=True)
    st.markdown("<div class='ips-title'>D.H.R.U.V.A.</div>", unsafe_allow_html=True)
    st.markdown("<div class='ips-subtitle'>National Research & Anomaly Society</div>", unsafe_allow_html=True)
    st.markdown("<div class='ips-motto'>\"Fear is just missing data. Logic is the cure.\"</div>", unsafe_allow_html=True)

# 4. TABS
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
                <p style='font-style:italic; font-size:18px; color:#DDD;'>"Ghosts or consciousness survive physical death. Paranormal activity is independent of time."</p>
                <p style='color:#00D4FF; font-weight:bold; margin-bottom:0;'>- Late Rev. Gaurav Tiwari</p>
                <p style='color:#555; font-size:12px;'>Founder, Indian Paranormal Society</p>
                <p style='margin-top:15px; color:#AAA;'>His dedication to replacing fear with logic is the driving force behind D.H.R.U.V.A.</p>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 style='font-family:Cinzel;'>THE DIRECTORATE</h2>", unsafe_allow_html=True)
    col_dir1, col_dir2 = st.columns([1, 2])
    with col_dir1:
        try: st.image("director.png", width=300)
        except: st.info("Founder Photo")
    with col_dir2:
        st.markdown("<h3 style='color:#00D4FF !important;'>Pranav Anil Rahane</h3>", unsafe_allow_html=True)
        st.caption("Founder & Chief Investigator | CSE (AI & DS), IIIT Kottayam")
        st.write("D.H.R.U.V.A. (Digital Holistic Residual Unexplained Variable Analysis) is a youth-led unit bridging folklore and modern science.")
        st.write("Based in Maharashtra, currently operating from IIIT Kottayam.")

with tab3:
    if conn:
        try:
            df_inv = conn.read(worksheet="Investigations", ttl=0)
            if not df_inv.empty:
                for _, row in df_inv.iterrows():
                    st.markdown(f"<div class='ips-block'><h4>{row['Title']}</h4><p>{row['Details']}</p><b>VERDICT: {row['Verdict']}</b></div>", unsafe_allow_html=True)
            else: st.info("No declassified files yet.")
        except: st.info("Connecting to secure archives...")

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
                    st.success("INTEL RECEIVED AT D.H.R.U.V.A. HQ.")
                except Exception as e: st.error(f"Transmission failed: {e}")

with tab5:
    st.markdown(f'<div class="green-box-container"><div style="color:#555; text-align:left; font-size:12px;">Email:</div><a href="mailto:team.dhruva.research@gmail.com" class="email-text">✉️ team.dhruva.research@gmail.com</a></div>', unsafe_allow_html=True)
    with st.form("contact_form", clear_on_submit=True):
        st.markdown("<h3 style='font-family:Cinzel;'>DIRECT CONTACT</h3>", unsafe_allow_html=True)
        cn = st.text_input("FULL NAME *"); n = st.text_input("Number"); ce = st.text_input("EMAIL *"); cm = st.text_area("MESSAGE *")
        if st.form_submit_button("SEND MESSAGE"):
            if ce and cm and conn:
                new_msg = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "FULL_NAME": cn, "Number": n, "EMAIL": ce, "MESSAGE": cm
                }])
                try:
                    ex = conn.read(worksheet="Messages", ttl=0)
                    up = pd.concat([ex, new_msg], ignore_index=True)
                    conn.update(worksheet="Messages", data=up)
                    st.success("MESSAGE TRANSMITTED.")
                except Exception as e: st.error(f"Error: {e}")

# 5. HIDDEN HQ CONTROL
if access_code == "classified":
    with st.sidebar:
        st.markdown("### 🔐 HQ CONTROL")
        if not st.session_state['auth']:
            u = st.text_input("ID"); p = st.text_input("KEY", type="password")
            if st.button("LOGIN"):
                if u == "Pranav" and p == "DhruvaBot": st.session_state['auth'] = True; st.rerun()
        if st.session_state['auth']:
            st.success("DIRECTOR ONLINE")
            
            # --- VIEW DATA ---
            if st.checkbox("📥 VIEW REPORTS"):
                st.dataframe(conn.read(worksheet="Reports", ttl=0))
            if st.checkbox("✉️ VIEW MESSAGES"):
                st.dataframe(conn.read(worksheet="Messages", ttl=0))

            # --- PUBLISH CASE ---
            with st.expander("📤 PUBLISH NEW CASE"):
                with st.form("pub_case"):
                    mt = st.text_input("Title"); ms = st.selectbox("Verdict", ["SOLVED", "UNEXPLAINED"]); md = st.text_area("Details")
                    if st.form_submit_button("GO LIVE"):
                        new_c = pd.DataFrame([{"Title": mt, "Verdict": ms, "Details": md, "Date": str(datetime.date.today())}])
                        try:
                            ex = conn.read(worksheet="Investigations", ttl=0)
                            up = pd.concat([ex, new_c], ignore_index=True)
                            conn.update(worksheet="Investigations", data=up)
                            st.success("Case Published.")
                        except Exception as e: st.error(f"DB Error: {e}")
            
            if st.button("LOGOUT"): st.session_state['auth'] = False; st.rerun()

st.markdown("<div style='text-align:center; color:#333; font-size:12px; padding:40px;'>© 2026 D.H.R.U.V.A. | LOGIC OVER FEAR</div>", unsafe_allow_html=True)
