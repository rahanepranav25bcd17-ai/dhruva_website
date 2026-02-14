import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
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
    st.error(f"UPLINK FAILED: Check requirements.txt and Secrets. Error: {e}")

# --- AUTH STATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
access_code = st.query_params.to_dict().get("access")

# --- PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Raleway:wght@300;400&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Raleway', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0A0A0A; border-bottom: 1px solid #111; justify-content: center; }
    .stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
    .ips-title { font-family: 'Cinzel', serif; font-size: 55px; text-align: center; letter-spacing: 5px; }
    .ips-subtitle { font-family: 'Raleway', sans-serif; font-size: 14px; text-align: center; color: #00D4FF; letter-spacing: 4px; }
    .ips-motto { text-align: center; color: #00D4FF; font-style: italic; font-weight: bold; margin-bottom: 30px; }
    .ips-block { background-color: #0A0A0A; border-left: 3px solid #00D4FF; padding: 30px; margin: 30px 0; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
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
    c1, c2 = st.columns([1, 2])
    with c1:
        try: st.image("gaurav_tiwari.png", use_container_width=True)
        except: st.info("Inspiration: Late Rev. Gaurav Tiwari")
    with c2:
        st.markdown("<div class='ips-block'><h3>OUR INSPIRATION</h3><p style='font-style:italic;'>\"Ghosts or consciousness survive physical death.\"</p><b>- Late Rev. Gaurav Tiwari</b></div>", unsafe_allow_html=True)

with tab4:
    with st.form("anomaly_form", clear_on_submit=True):
        fn = st.text_input("FULL NAME *"); ph = st.text_input("CONTACT NO *")
        lc = st.text_input("LOCATION *"); ct = st.selectbox("CATEGORY", ["Haunting", "UFO", "Other"])
        ds = st.text_area("DETAILED DESCRIPTION *")
        if st.form_submit_button("TRANSMIT INTEL"):
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

# --- HQ CONTROL ---
if access_code == "classified":
    with st.sidebar:
        st.markdown("### 🔐 HQ CONTROL")
        if not st.session_state['auth']:
            u = st.text_input("ID"); p = st.text_input("KEY", type="password")
            if st.button("LOGIN"):
                if u == "Pranav" and p == "DhruvaBot": st.session_state['auth'] = True; st.rerun()
        if st.session_state['auth']:
            st.success("DIRECTOR ONLINE")
            with st.expander("📤 PUBLISH CASE"):
                with st.form("pub_case"):
                    mt = st.text_input("Title"); ms = st.selectbox("Verdict", ["SOLVED", "UNEXPLAINED"]); md = st.text_area("Details")
                    if st.form_submit_button("PUBLISH"):
                        if conn:
                            new_c = pd.DataFrame([{"Title": mt, "Verdict": ms, "Details": md, "Date": str(datetime.date.today())}])
                            try:
                                ex = conn.read(worksheet="Investigations", ttl=0)
                                up = pd.concat([ex, new_c], ignore_index=True)
                                conn.update(worksheet="Investigations", data=up)
                                st.success("Case Published.")
                            except Exception as e: st.error(f"Database error: {e}")
