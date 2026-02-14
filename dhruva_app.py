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
    .stTabs [data-baseweb="tab-list"] { background-color: #0A0A0A; justify-content: center; border-bottom: 1px solid #1A1A1A; }
    .stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
    .ips-title { font-family: 'Cinzel', serif; font-size: 55px; text-align: center; letter-spacing: 5px; margin-bottom: 0; color: #FFFFFF; }
    .ips-motto { text-align: center; color: #00D4FF; font-style: italic; font-weight: bold; margin-bottom: 30px; font-size: 16px; }
    .footer-container { background-color: #0A0A0A; border-top: 1px solid #1A1A1A; padding: 40px 20px; margin-top: 60px; color: #AAA; }
    .footer-title { font-family: 'Cinzel', serif; color: #FFF; font-size: 18px; letter-spacing: 2px; margin-bottom: 15px; }
    .footer-link { color: #AAA; text-decoration: none; display: block; margin: 8px 0; font-size: 14px; }
    .footer-link:hover { color: #00D4FF; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
col_h1, col_h2, col_h3 = st.columns([1, 4, 1])
with col_h2:
    try: st.image("logo.png", width=150)
    except: st.markdown("<h1 style='text-align:center;'>🦅</h1>", unsafe_allow_html=True)
    st.markdown("<div class='ips-title'>D.H.R.U.V.A.</div>", unsafe_allow_html=True)
    st.markdown("<div class='ips-motto'>\"Fear is just missing data. Logic is the cure.\"</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["HOME", "ABOUT US", "INVESTIGATIONS", "REPORT MYSTERY", "CONTACT"])

# ... (Previous tab logic for HOME, ABOUT, INVESTIGATIONS, REPORT remains the same) ...

with tab5:
    st.markdown("<h2 style='font-family:Cinzel;'>CONTACT HQ</h2>", unsafe_allow_html=True)
    st.markdown('<div style="background-color:#0A0A0A; border:1px solid #1A1A1A; padding:30px; text-align:center;"><a href="mailto:team.dhruva.research@gmail.com" style="color:#2ECC71; font-weight:bold; font-size:20px; text-decoration:none;">✉️ team.dhruva.research@gmail.com</a></div>', unsafe_allow_html=True)
    with st.form("contact"):
        cn = st.text_input("NAME *"); ce = st.text_input("EMAIL *"); cm = st.text_area("MESSAGE *")
        if st.form_submit_button("SEND"):
            if ce and cm and conn:
                new_m = pd.DataFrame([{"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "FULL_NAME": cn, "EMAIL": ce, "MESSAGE": cm}])
                try:
                    ex = conn.read(worksheet="Messages", ttl=0); up = pd.concat([ex, new_m], ignore_index=True); conn.update(worksheet="Messages", data=up)
                    st.success("TRANSMITTED.")
                except Exception as e: st.error(f"Error: {e}")

# --- 4. THE IPS-STYLE VISUAL FOOTER ---
st.markdown("<div class='footer-container'>", unsafe_allow_html=True)
f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1.5])

with f_col1:
    st.markdown("<div class='footer-title'>INDIAN PARANORMAL SOCIETY</div>", unsafe_allow_html=True)
    st.write("Investigating the unexplained and documenting paranormal phenomena across India since 2026.")
    st.markdown("<p style='font-style:italic; color:#00D4FF;'>\"We don't chase ghosts. We investigate them.\"</p>", unsafe_allow_html=True)

with f_col2:
    st.markdown("<div class='footer-title'>QUICK LINKS</div>", unsafe_allow_html=True)
    st.markdown("<a class='footer-link' href='#'>About Us</a>", unsafe_allow_html=True)
    st.markdown("<a class='footer-link' href='#'>Investigations</a>", unsafe_allow_html=True)
    st.markdown("<a class='footer-link' href='#'>Contact</a>", unsafe_allow_html=True)

with f_col3:
    st.markdown("<div class='footer-title'>RESOURCES</div>", unsafe_allow_html=True)
    st.markdown("<a class='footer-link' href='#'>Report Anomaly</a>", unsafe_allow_html=True)
    st.markdown("<a class='footer-link' href='#'>Case Files</a>", unsafe_allow_html=True)

with f_col4:
    st.markdown("<div class='footer-title'>CONNECT WITH US</div>", unsafe_allow_html=True)
    c_sub1, c_sub2 = st.columns(2)
    with c_sub1:
        try: st.image("insta_qr.png", caption="Scan for Instagram", width=100) # cite: WhatsApp Image 2026-02-14 at 5.17.06 PM.jpeg
        except: st.write("Instagram QR")
    with c_sub2:
        try: st.image("logo.png", width=80)
        except: st.write("🦅")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; font-size:12px; color:#444; padding-bottom:20px;'>© 2026 D.H.R.U.V.A. | Designed & Developed by Pranav Rahane</div>", unsafe_allow_html=True)

# --- 5. HIDDEN HQ CONTROL (Sidebar remains the same) ---
