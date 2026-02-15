import streamlit as st
import pandas as pd
import datetime

# 1. PAGE CONFIG
st.set_page_config(
    page_title="D.H.R.U.V.A.",
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

# 2. CSS STYLING
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Raleway:wght@300;400&display=swap');
.stApp { background-color: #000000; color: #FFFFFF; font-family: 'Raleway', sans-serif; }
.stTabs [data-baseweb="tab-list"] { background-color: #0A0A0A; justify-content: center; border-bottom: 1px solid #1A1A1A; }
.stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
.ips-title { font-family: 'Cinzel', serif; font-size: 55px; text-align: center; letter-spacing: 5px; color: #FFFFFF; }
.ips-motto { text-align: center; color: #00D4FF; font-style: italic; font-weight: bold; margin-bottom: 30px; }
.ips-block { background-color: #0A0A0A; border-left: 3px solid #00D4FF; padding: 30px; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# 3. HEADER
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
    st.markdown("<h2 style='font-family:Cinzel; color:white;'>THE DIRECTORATE</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1: 
        try: st.image("director.png", width=300)
        except: st.info("Pranav Anil Rahane")
    with c2:
        st.markdown("<h3 style='color:#00D4FF;'>Pranav Anil Rahane</h3>", unsafe_allow_html=True)
        st.write("Founder & Chief Investigator | CSE (AI & DS), IIIT Kottayam")
        st.write("D.H.R.U.V.A. (Digital Holistic Residual Unexplained Variable Analysis) is a youth-led unit bridging folklore and modern science.")
    
    st.markdown("---")
    st.markdown("<h2 style='font-family:Cinzel; text-align:center;'>FIELD TEAM</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    for i, col in enumerate([t1, t2, t3]):
        with col:
            try: st.image(f"member{i+1}.png")
            except: st.markdown("<div style='background-color:#0A0A0A; border:1px solid #1A1A1A; padding:20px; text-align:center; border-radius:10px;'>👤 Awaiting Personnel</div>", unsafe_allow_html=True)
            m = st.session_state['team'][f"m{i+1}"]
            st.markdown(f"**{m['name']}**")
            st.caption(m['bio'])

with tab3:
    st.markdown("<h2 style='font-family:Cinzel;'>INVESTIGATION ARCHIVES</h2>", unsafe_allow_html=True)
    st.info("⚠️ SCANNING FOR DECLASSIFIED INTEL...")
    st.markdown("""<div class='ips-block'><b>STATUS: INITIAL PHASE</b><br>D.H.R.U.V.A. is currently active at multiple undisclosed locations. We are analyzing residual variables. Case files will remain encrypted until final verification.</div>""", unsafe_allow_html=True)
    
    if conn:
        try:
            df = conn.read(worksheet="Investigations", ttl=0)
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
    st.markdown("<h2 style='font-family:Cinzel;'>CONTACT HQ</h2>", unsafe_allow_html=True)
    st.markdown('<div style="background-color:#0A0A0A; border:1px solid #1A1A1A; padding:30px; text-align:center;"><a href="mailto:team.dhruva.research@gmail.com" style="color:#2ECC71; font-weight:bold; font-size:20px; text-decoration:none;">✉️ team.dhruva.research@gmail.com</a></div>', unsafe_allow_html=True)

# --- 4. THE FOOTER (NO INDENTATION TO FIX BUG) ---
footer_html = """<style>
.footer-container { background-color: #111; border-top: 1px solid #222; padding: 60px 20px; margin-top: 80px; font-family: 'Raleway', sans-serif; display: flex; flex-wrap: wrap; justify-content: space-between; }
.footer-col { flex: 1; min-width: 250px; margin-bottom: 20px; padding: 0 10px; }
.footer-title { font-family: 'Cinzel', serif; color: #FFF; font-size: 16px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
.footer-text { color: #AAA; font-size: 14px; line-height: 1.6; }
.footer-link { display: block; color: #AAA; text-decoration: none; margin-bottom: 8px; font-size: 14px; transition: 0.3s; }
.footer-link:hover { color: #00D4FF; padding-left: 5px; }
.social-icons { display: flex; gap: 15px; margin-top: 10px; }
.social-circle { width: 35px; height: 35px; border: 1px solid #555; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #AAA; text-decoration: none; transition: 0.3s; }
.social-circle:hover { border-color: #00D4FF; color: #00D4FF; }
</style>
<div class="footer-container">
<div class="footer-col" style="flex: 2; padding-right: 40px;">
<div class="footer-title">D.H.R.U.V.A. RESEARCH GROUP</div>
<div class="footer-text">
Investigating the unexplained and documenting paranormal phenomena across India using scientific methodologies since 2026.
<br><br>
<i style="color:#00D4FF;">"Where science meets the unknown."</i>
</div>
</div>
<div class="footer-col">
<div class="footer-title">QUICK LINKS</div>
<a href="#" class="footer-link">About Us</a>
<a href="#" class="footer-link">Investigations</a>
<a href="#" class="footer-link">Report an Incident</a>
<a href="#" class="footer-link">Case Files</a>
<a href="#" class="footer-link">Contact</a>
</div>
<div class="footer-col">
<div class="footer-title">CONNECT WITH US</div>
<div class="social-icons">
<a href="https://www.instagram.com/dhruva.research" target="_blank" class="social-circle">📷</a>
<a href="#" class="social-circle">f</a>
<a href="#" class="social-circle">▶</a>
<a href="#" class="social-circle">🐦</a>
</div>
</div>
</div>
<div style="text-align:center; color:#444; font-size:12px; padding:20px; border-top:1px solid #222; background-color:#111;">
© 2026 D.H.R.U.V.A. Research Group. All rights reserved. | Designed by Pranav Rahane
</div>"""

st.markdown(footer_html, unsafe_allow_html=True)

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
            with st.expander("👥 TEAM MANAGEMENT"):
                for i in range(1, 4):
                    mk = f"m{i}"
                    st.session_state['team'][mk]['name'] = st.text_input(f"Member {i} Name", st.session_state['team'][mk]['name'])
                    st.session_state['team'][mk]['bio'] = st.text_area(f"Member {i} Info", st.session_state['team'][mk]['bio'])
            if st.button("LOGOUT"): st.session_state['auth'] = False; st.rerun()
