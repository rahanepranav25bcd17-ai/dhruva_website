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
    .ips-block { background-color: #0A0A0A; border-left: 3px solid #00D4FF; padding: 30px; margin: 20px 0; border-radius: 0 10px 10px 0; }
    .team-card { background-color: #0A0A0A; border: 1px solid #1A1A1A; padding: 20px; text-align: center; border-radius: 10px; }
    
    /* Footer Style */
    .footer-container { background-color: #0A0A0A; border-top: 1px solid #1A1A1A; padding: 40px 20px; margin-top: 60px; color: #AAA; }
    .footer-title { font-family: 'Cinzel', serif; color: #FFF; font-size: 20px; letter-spacing: 2px; }
    .footer-link { color: #AAA; text-decoration: none; display: block; margin: 8px 0; font-size: 14px; }
    .footer-link:hover { color: #00D4FF; }
    .social-icon { width: 24px; margin-right: 15px; opacity: 0.7; transition: 0.3s; }
    .social-icon:hover { opacity: 1; transform: scale(1.1); }
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
        st.markdown("<div class='ips-block'><h3>OUR INSPIRATION</h3><p>\"Ghosts or consciousness survive physical death. Paranormal activity is independent of time.\"</p><b>- Late Rev. Gaurav Tiwari</b><br><small>Founder, Indian Paranormal Society</small></div>", unsafe_allow_html=True)

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
            except: st.markdown("<div class='team-card'>👤 Awaiting Personnel</div>", unsafe_allow_html=True)
            m = st.session_state['team'][f"m{i+1}"]
            st.markdown(f"**{m['name']}**")
            st.caption(m['bio'])

with tab3:
    st.markdown("<h2 style='font-family:Cinzel;'>INVESTIGATION ARCHIVES</h2>", unsafe_allow_html=True)
    st.info("⚠️ SCANNING FOR DECLASSIFIED INTEL...")
    st.write("D.H.R.U.V.A. is currently in the initial phase of operation. We are analyzing multiple residual variables across active sites. Log in to HQ for live status.")
    if conn:
        try:
            df = conn.read(worksheet="Investigations", ttl=0)
            if not df.empty:
                for _, row in df.iterrows():
                    st.markdown(f"<div class='ips-block'><h4>{row['Title']}</h4><p>{row['Details']}</p><b>{row['Verdict']}</b></div>", unsafe_allow_html=True)
        except: pass

with tab5:
    st.markdown("<h2 style='font-family:Cinzel;'>CONTACT HQ</h2>", unsafe_allow_html=True)
    st.markdown('<div style="background-color:#0A0A0A; border:1px solid #1A1A1A; padding:30px; text-align:center;"><a href="mailto:team.dhruva.research@gmail.com" style="color:#2ECC71; font-weight:bold; font-size:20px; text-decoration:none;">✉️ team.dhruva.research@gmail.com</a></div>', unsafe_allow_html=True)
    with st.form("contact"):
        st.markdown("<h3 style='font-family:Cinzel;'>DIRECT MESSAGE</h3>", unsafe_allow_html=True)
        cn = st.text_input("NAME *"); ce = st.text_input("EMAIL *"); cm = st.text_area("MESSAGE *")
        if st.form_submit_button("SEND"):
            if ce and cm and conn:
                new_m = pd.DataFrame([{"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "FULL_NAME": cn, "EMAIL": ce, "MESSAGE": cm}])
                try:
                    ex = conn.read(worksheet="Messages", ttl=0); up = pd.concat([ex, new_m], ignore_index=True); conn.update(worksheet="Messages", data=up)
                    st.success("TRANSMITTED.")
                except Exception as e: st.error(f"Error: {e}")

# --- 4. IPS STYLE FOOTER ---
st.markdown("""
<div class="footer-container">
    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; max-width:1200px; margin:auto;">
        <div style="flex:1; min-width:300px; margin-bottom:30px;">
            <div class="footer-title">D.H.R.U.V.A. RESEARCH GROUP</div>
            <p style="font-size:13px; margin-top:15px; line-height:1.6;">Investigating the unexplained and documenting paranormal phenomena across India using scientific methodologies.</p>
            <p style="font-style:italic; font-size:14px; color:#00D4FF;">"Fear is just missing data."</p>
        </div>
        <div style="flex:1; min-width:200px; margin-bottom:30px;">
            <div class="footer-title">QUICK LINKS</div>
            <a href="#" class="footer-link">About Us</a>
            <a href="#" class="footer-link">Investigations</a>
            <a href="#" class="footer-link">Report an Incident</a>
            <a href="#" class="footer-link">Contact</a>
        </div>
        <div style="flex:1; min-width:200px; margin-bottom:30px;">
            <div class="footer-title">CONNECT WITH US</div>
            <div style="margin-top:20px;">
                <a href="https://www.instagram.com/dhruva.research"><img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" class="social-icon"></a>
                <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" class="social-icon"></a>
                <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" class="social-icon"></a>
            </div>
        </div>
    </div>
    <div style="text-align:center; margin-top:40px; border-top:1px solid #222; padding-top:20px; font-size:12px;">
        © 2026 D.H.R.U.V.A. Research Group. All rights reserved. | Designed & Developed by Pranav Rahane
    </div>
</div>
""", unsafe_allow_html=True)

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
