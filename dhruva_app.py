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
        "m1": {"name": "Agent Alpha", "bio": "Specialist in Thermal Imaging & EMF Analysis."},
        "m2": {"name": "Agent Beta", "bio": "Historian & Occult Researcher."},
        "m3": {"name": "Agent Gamma", "bio": "Tech Support & Drone Operator."}
    }

access_code = st.query_params.to_dict().get("access")

# 2. CSS STYLING
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Raleway:wght@300;400&display=swap');
.stApp { background-color: #000000; color: #FFFFFF; font-family: 'Raleway', sans-serif; }
.stTabs [data-baseweb="tab-list"] { background-color: #0A0A0A; justify-content: center; border-bottom: 1px solid #1A1A1A; }
.stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
.ips-title { font-family: 'Cinzel', serif; font-size: 55px; text-align: center; letter-spacing: 5px; color: #FFFFFF; }
.ips-motto { text-align: center; color: #00D4FF; font-style: italic; font-weight: bold; margin-bottom: 30px; }
.ips-block { background-color: #0A0A0A; border-left: 3px solid #00D4FF; padding: 30px; margin: 20px 0; }
.info-box { background-color: #111; padding: 20px; border: 1px solid #222; margin-bottom: 15px; border-radius: 5px; }
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

# --- TAB 1: HOME ---
with tab1:
    st.markdown("<h2 style='font-family:Cinzel; text-align:center; margin-bottom:40px;'>THE BRIDGE BETWEEN MYTH AND SCIENCE</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='ips-block'>
        <h3 style='color:#00D4FF; font-family:Cinzel;'>OUR CORE MISSION</h3>
        <p style='font-size:16px; line-height:1.6;'>
            D.H.R.U.V.A. (Digital Holistic Residual Unexplained Variable Analysis) is India's premier youth-led research initiative dedicated to the scientific study of anomalous phenomena. 
            We operate on the boundary where folklore ends and empirical evidence begins.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("""<div class='info-box'><h4 style='color:#00D4FF;'>🕵️‍♂️ WHAT WE DO</h4><ul><li>Scientific Investigation of Haunted Locations</li><li>UFO & Aerial Phenomenon Documentation</li><li>Debunking Superstitions through Logic</li></ul></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='info-box'><h4 style='color:#00D4FF;'>🔬 OUR APPROACH</h4><ul><li>Environmental Monitoring (EMF, Temperature)</li><li>Audio/Visual Analysis (EVP, Spectrum)</li><li>Data-Driven Conclusion</li></ul></div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_i1, col_i2 = st.columns([1, 3])
    with col_i1:
        try: st.image("gaurav_tiwari.png", caption="Late Rev. Gaurav Tiwari", use_container_width=True)
        except: st.info("Late Rev. Gaurav Tiwari")
    with col_i2:
        st.markdown("""<div class='ips-block'><h3 style='font-family:Cinzel;'>OUR ETERNAL INSPIRATION</h3><p style='font-size:18px; font-style:italic; color:#AAA;'>"Ghosts or consciousness survive physical death. Paranormal activity is independent of time."</p><p style='color:#00D4FF; font-weight:bold; margin-top:10px;'>- Late Rev. Gaurav Tiwari</p></div>""", unsafe_allow_html=True)

# --- TAB 2: ABOUT US (UPDATED WITH IMAGE PLACEHOLDERS) ---
with tab2:
    st.markdown("<h2 style='font-family:Cinzel; color:white; text-align:center;'>THE DIRECTORATE</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1: 
        try: st.image("director.png", width=300)
        except: st.info("Pranav Anil Rahane")
    with c2:
        st.markdown("<h3 style='color:#00D4FF; font-family:Cinzel; font-size:30px;'>Pranav Anil Rahane</h3>", unsafe_allow_html=True)
        st.markdown("**Founder & Chief Investigator** | *CSE (AI & DS), IIIT Kottayam*")
        st.markdown("""<div style='background-color:#111; padding:20px; border-radius:5px; margin-top:20px; border-left:3px solid #00D4FF;'><p>"I founded D.H.R.U.V.A. with a singular vision: to strip away the fear associated with the unknown. We are not ghost hunters; we are anomaly researchers."</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2 style='font-family:Cinzel; text-align:center;'>FIELD OPERATIONS TEAM</h2>", unsafe_allow_html=True)
    
    # --- UPDATED TEAM SECTION WITH IMAGE PLACEHOLDERS ---
    t1, t2, t3 = st.columns(3)
    for i, col in enumerate([t1, t2, t3]):
        with col:
            # Try to load member image, if not found, load GENERIC AGENT image
            try: 
                st.image(f"member{i+1}.png", use_container_width=True)
            except: 
                # This is the "Place" you wanted - a silhouette image
                st.image("https://cdn-icons-png.flaticon.com/512/3237/3237472.png", width=150, caption="Classified Personnel")
            
            m = st.session_state['team'][f"m{i+1}"]
            st.markdown(f"<h4 style='text-align:center; color:#00D4FF;'>{m['name']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; font-size:13px; color:#AAA;'>{m['bio']}</p>", unsafe_allow_html=True)

# --- TAB 3: INVESTIGATIONS ---
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

# --- TAB 4: REPORT MYSTERY ---
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

# --- TAB 5: CONTACT ---
with tab5:
    st.markdown("<h2 style='font-family:Cinzel;'>CONTACT HQ</h2>", unsafe_allow_html=True)
    st.markdown('<div style="background-color:#0A0A0A; border:1px solid #1A1A1A; padding:30px; text-align:center;"><a href="mailto:team.dhruva.research@gmail.com" style="color:#2ECC71; font-weight:bold; font-size:20px; text-decoration:none;">✉️ team.dhruva.research@gmail.com</a></div>', unsafe_allow_html=True)

# --- FOOTER ---
footer_style = """
<style>
.footer-container { background-color: #111; border-top: 1px solid #222; padding: 60px 20px; margin-top: 80px; font-family: 'Raleway', sans-serif; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start;}
.footer-col { flex: 1; min-width: 300px; margin-bottom: 20px; padding: 0 20px; }
.footer-title { font-family: 'Cinzel', serif; color: #FFF; font-size: 18px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
.footer-text { color: #AAA; font-size: 14px; line-height: 1.6; }
.social-icons { display: flex; gap: 20px; margin-top: 15px; }
.social-circle { width: 50px; height: 50px; border: 1px solid #555; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #AAA; text-decoration: none; transition: 0.3s; font-size: 24px; }
.social-circle:hover { border-color: #00D4FF; color: #00D4FF; transform: scale(1.1); box-shadow: 0 0 10px rgba(0,212,255,0.3); }
</style>
"""
footer_content = """
<div class="footer-container">
<div class="footer-col" style="flex: 2;">
<div class="footer-title">D.H.R.U.V.A. RESEARCH GROUP</div>
<div class="footer-text">
Investigating the unexplained and documenting paranormal phenomena across India using scientific methodologies since 2026.
<br><br>
<i style="color:#00D4FF;">"Where science meets the unknown."</i>
</div>
</div>
<div class="footer-col" style="flex: 1; display:flex; flex-direction:column; align-items:center;">
<div class="footer-title">CONNECT WITH US</div>
<div class="social-icons" style="justify-content: center;">
<a href="https://www.instagram.com/dhruva.research_official?igsh=emQxMWMxcmNsYzA=" target="_blank" class="social-circle"><i class="fab fa-instagram"></i></a>
</div>
</div>
</div>
<div style="text-align:center; color:#444; font-size:12px; padding:20px; border-top:1px solid #222; background-color:#111;">
© 2026 D.H.R.U.V.A. Research Group. All rights reserved. | Designed by Pranav Rahane
</div>
"""
st.markdown(footer_style + footer_content, unsafe_allow_html=True)

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
            
            with st.expander("📩 INCOMING INTEL (Reports)"):
                try:
                    rep_df = conn.read(worksheet="Reports", ttl=0)
                    st.dataframe(rep_df)
                except: st.error("No reports found.")
            
            with st.expander("✉️ DIRECT MESSAGES"):
                try:
                    msg_df = conn.read(worksheet="Messages", ttl=0)
                    st.dataframe(msg_df)
                except: st.error("No messages found.")

            with st.expander("👥 TEAM MANAGEMENT"):
                st.info("Edit names below. (Resets on refresh)")
                for i in range(1, 4):
                    mk = f"m{i}"
                    st.session_state['team'][mk]['name'] = st.text_input(f"Member {i} Name", st.session_state['team'][mk]['name'])
                    st.session_state['team'][mk]['bio'] = st.text_area(f"Member {i} Info", st.session_state['team'][mk]['bio'])
            
            if st.button("LOGOUT"): st.session_state['auth'] = False; st.rerun()
