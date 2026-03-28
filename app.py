import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
import urllib.parse
import pandas as pd
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Elite Studio | AI Career Architect", page_icon="⚡", layout="wide")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please check your .env file or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. ELITE STUDIO PREMIUM CSS STYLING ---
st.markdown("""
<style>
    /* Import Fonts and Icons */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    html, body, p, span:not(.material-symbols-rounded):not([data-testid="stIconMaterial"]), div, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Inter', sans-serif !important;
    }
    
    .material-symbols-rounded, [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
    }

    /* Theme & Backgrounds */
    .stApp { background-color: #050814; color: #f0f6fc; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #0f1524 !important;
        color: #f0f6fc !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Elite Custom Cards */
    .zna-card {
        background: linear-gradient(145deg, #0f172a 0%, #0a0f1d 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 24px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .zna-card:hover {
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.3);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #050814 !important;
        border-right: 1px solid #1e293b;
        width: 300px !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span:not(.material-symbols-rounded), [data-testid="stSidebar"] label {
        color: #94a3b8 !important;
    }
    .sidebar-header { color: #475569; font-size: 11px; font-weight: 700; text-transform: uppercase; margin: 30px 0 15px 15px; letter-spacing: 1.5px;}

    .stRadio [data-testid="stMarkdownContainer"] {
        background-color: transparent !important;
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        padding: 12px 15px !important;
        display: flex; align-items: center; gap: 12px; transition: all 0.2s ease;
    }
    .stRadio label:hover [data-testid="stMarkdownContainer"] { background-color: #0f172a !important; color: #e2e8f0 !important;}
    .stRadio label[data-selected="true"] [data-testid="stMarkdownContainer"] {
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.1) 0%, transparent 100%) !important;
        border-left: 3px solid #3b82f6 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Live Pulse Animation */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
        70% { box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }
    .live-pulse {
        display: inline-block; width: 8px; height: 8px; border-radius: 50%;
        background-color: #22c55e; animation: pulse-green 2s infinite; margin-left: 6px;
    }
    .status-badge {
        background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2);
        color: #22c55e; padding: 6px 12px; border-radius: 50px; font-size: 10px; font-weight: 700;
        text-transform: uppercase; display: inline-flex; align-items: center; letter-spacing: 0.5px;
    }

    /* Buttons & Links */
    .stButton>button {
        border-radius: 50px !important;
        background: linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%) !important;
        color: white !important; font-weight: 600 !important; font-size: 14px !important;
        padding: 12px 28px !important; border: none !important; transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px); box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    }
    
    /* Global Job Portal Link Rules */
    .side-job-portal {
        border-radius: 12px; 
        text-align: center; 
        padding: 14px; 
        font-weight: 600; 
        cursor: pointer; 
        display: inline-block;
        width: 100%; 
        margin-top: 10px; 
        text-decoration: none; 
        transition: all 0.3s ease; 
        font-size: 13px;
        color: white !important; /* Force all text to white */
    }
    .side-job-portal:hover { 
        filter: brightness(1.2); 
        box-shadow: 0 0 15px rgba(255,255,255,0.2); 
    }

    /* Steps UI */
    .zna-steps { display: flex; justify-content: space-around; margin-bottom: 30px; position: relative; }
    .zna-step-node { display: flex; flex-direction: column; align-items: center; width: 33%; position: relative; z-index: 2; }
    .zna-steps::before { content: ''; position: absolute; height: 2px; background: #1e293b; width: 66%; top: 16px; left: 17%; z-index: 1; }
    .zna-step-circle { width: 34px; height: 34px; border-radius: 50%; background: #0f1524; border: 2px solid #1e293b; color: #64748b; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; margin-bottom: 10px; transition: all 0.3s ease; }
    .step-active .zna-step-circle { background: #3b82f6; border-color: #3b82f6; color: white; box-shadow: 0 0 15px rgba(59,130,246,0.4); }
    .zna-step-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #64748b; }
    .step-active .zna-step-label { color: #f8fafc; }
    
</style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def get_gemini_response(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {str(e)}"

def sanitize_text(text):
    return text.encode('latin-1', 'ignore').decode('latin-1')

def create_professional_pdf(text_content, title="Document", email="", phone="", linkedin="", github=""):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=title, ln=True, align='C')
    pdf.set_font("Arial", size=10)
    if email:
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 5, txt=f"Email: {sanitize_text(email)}", ln=True, align='C', link=f"mailto:{email}")
    if phone:
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 5, txt=f"Phone: {sanitize_text(phone)}", ln=True, align='C', link=f"tel:{phone.replace(' ', '')}")
    if linkedin:
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 5, txt="LinkedIn Profile", ln=True, align='C', link=linkedin)
    if github:
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 5, txt="GitHub Portfolio", ln=True, align='C', link=github)
    pdf.set_text_color(0, 0, 0)
    pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
    pdf.ln(8)
    pdf.set_font("Arial", size=11)
    for line in text_content.split('\n'):
        clean_line = sanitize_text(line)
        if len(clean_line) < 60 and clean_line.isupper() and len(clean_line.strip()) > 0:
            pdf.set_font("Arial", 'B', 12)
            pdf.ln(5)
            pdf.cell(0, 8, txt=clean_line, ln=True)
            pdf.set_font("Arial", size=11)
        else:
            pdf.multi_cell(0, 6, txt=clean_line)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. SESSION STATE INITIALIZATION ---
if 'resume_text' not in st.session_state: st.session_state['resume_text'] = ""
if 'target_job' not in st.session_state: st.session_state['target_job'] = ""
if 'user_name' not in st.session_state: st.session_state['user_name'] = "Professional Resume"
if 'user_email' not in st.session_state: st.session_state['user_email'] = ""
if 'user_phone' not in st.session_state: st.session_state['user_phone'] = ""
if 'user_linkedin' not in st.session_state: st.session_state['user_linkedin'] = ""
if 'user_github' not in st.session_state: st.session_state['user_github'] = ""

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px;">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 20px; box-shadow: 0 4px 10px rgba(59,130,246,0.3);">Z</div>
            <div style="font-size: 22px; font-weight: 800; letter-spacing: -0.5px; color: white;">Elite Studio</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-header'>Workspace</div>", unsafe_allow_html=True)
    app_mode = st.radio("", [
        "📊 Dashboard", 
        "📄 Resume Builder", 
        "✉️ Letter Engine", 
        "🔍 ATS Scanner",
        "🎙️ Interview Prep",
        "🗺️ Skill Gap Analyzer" 
    ])
    st.markdown("---")
    
    st.markdown("""
        <div style='background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 20px; margin-top: 20px;'>
            <div style='font-size: 11px; font-weight: 700; color: #3b82f6; text-transform: uppercase; margin-bottom: 8px;'>PRO WORKSPACE</div>
            <div style='font-size: 12px; color: #64748b; line-height: 1.5;'>Personalize your profile to unlock job-specific insights.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-header'>🌐 Direct Apply Portals</div>", unsafe_allow_html=True)
    
    if st.session_state['target_job']:
        linkedin_query = urllib.parse.quote(st.session_state['target_job'])
        indeed_query = urllib.parse.quote(st.session_state['target_job'])
        naukri_query = st.session_state['target_job'].replace(' ', '-').lower()
        
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; gap: 5px; margin-top: 10px;">
            <a href="https://www.linkedin.com/jobs/search/?keywords={linkedin_query}" target="_blank" class="side-job-portal" style="background: #0a66c2; border: none;">
                <i class="fab fa-linkedin" style="margin-right: 8px;"></i> LinkedIn ↗
            </a>
            <a href="https://in.indeed.com/jobs?q={indeed_query}" target="_blank" class="side-job-portal" style="background: #2557a7; border: none;">
                <i class="fas fa-info-circle" style="margin-right: 8px;"></i> Indeed ↗
            </a>
            <a href="https://www.naukri.com/{naukri_query}-jobs" target="_blank" class="side-job-portal" style="background: #0075FF; border: none;">
                <i class="fas fa-briefcase" style="margin-right: 8px;"></i> Naukri ↗
            </a>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"Searching roles for: **{st.session_state['target_job']}**")
    else:
        st.info("💡 Fill out the 'Target Role' in the Resume Builder to unlock live Job Portals.")

# --- 6. MAIN APP LOGIC ---

if app_mode == "📊 Dashboard":
    st.markdown("<div style='float: right;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 32px; font-weight: 800; margin-bottom: 5px;'>Welcome to your Career Workspace</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px;'>Your central hub for AI-powered career growth and optimization.</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown("<div class='zna-card'><div style='font-size:12px; color:#64748b; font-weight:bold;'>TEMPLATES</div><div style='font-size:24px; font-weight:bold; margin-top:5px;'>3 Styles</div></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='zna-card'><div style='font-size:12px; color:#64748b; font-weight:bold;'>INPUT MODES</div><div style='font-size:24px; font-weight:bold; margin-top:5px;'>Dual Auth</div></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='zna-card'><div style='font-size:12px; color:#64748b; font-weight:bold;'>INTERVIEW AI</div><div style='font-size:24px; font-weight:bold; margin-top:5px;'>Active</div></div>", unsafe_allow_html=True)
    with col4: st.markdown("<div class='zna-card'><div style='font-size:12px; color:#64748b; font-weight:bold;'>ATS SCANNER</div><div style='font-size:24px; font-weight:bold; margin-top:5px;'>Semantic</div></div>", unsafe_allow_html=True)
    
    dash_col1, dash_col2 = st.columns([0.65, 0.35])
    with dash_col1:
        st.markdown("<div class='zna-card'><div style='font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;'><i class='fas fa-chart-area' style='color:#3b82f6;'></i> ATS Optimization Trends</div>", unsafe_allow_html=True)
        chart_data = pd.DataFrame([65, 72, 68, 85, 88, 92, 96], columns=["Match Score (%)"])
        st.line_chart(chart_data, color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    with dash_col2:
        st.markdown("<div class='zna-card' style='height: 100%;'><div style='font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;'><i class='fas fa-terminal' style='color:#8b5cf6;'></i> Live System Logs</div>", unsafe_allow_html=True)
        st.info("✅ **[SYSTEM]** LLM Engine connected.")
        if st.session_state['resume_text']:
            st.success("✅ **[MEMORY]** Profile loaded securely.")
        else:
            st.warning("⏳ **[MEMORY]** Awaiting user input...")
        if st.session_state['target_job']:
            st.info(f"🎯 **[TARGET]** {st.session_state['target_job']}")
        st.markdown("</div>", unsafe_allow_html=True)

elif app_mode == "📄 Resume Builder":
    st.markdown("<div style='float: right;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: #0f172a; border: 1px solid #1e293b; padding: 12px; border-radius: 12px;'><i class='fas fa-microchip' style='color: #3b82f6; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>Smart Resume Builder</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>AI-powered synthesis of your professional data.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Setup & Context", "📄 Synthesis Output"])
    
    with tab1:
        st.markdown("<div class='zna-card'>", unsafe_allow_html=True)
        st.markdown("""
            <div class='zna-steps'>
                <div class='zna-step-node step-active'><div class='zna-step-circle'>1</div><div class='zna-step-label'>Context</div></div>
                <div class='zna-step-node step-inactive'><div class='zna-step-circle'>2</div><div class='zna-step-label'>Analysis</div></div>
                <div class='zna-step-node step-inactive'><div class='zna-step-circle'>3</div><div class='zna-step-label'>Synthesis</div></div>
            </div>
        """, unsafe_allow_html=True)
        
        style = st.selectbox("Select Template Architecture:", ["Standard Corporate", "Executive & Leadership", "Creative & Tech", "Academic & Research"])
        input_method = st.radio("Data Injection Mode:", ["⚡ Auto-Parse (Raw Data)", "✍️ Manual Entry (Structured)"], horizontal=True)
        
        if input_method == "⚡ Auto-Parse (Raw Data)":
            col_a, col_b = st.columns(2)
            with col_a:
                auto_name = st.text_input("Full Name *", key="auto_name")
                auto_email = st.text_input("Email", key="auto_email")
                auto_github = st.text_input("GitHub URL", key="auto_github")
            with col_b:
                auto_target = st.text_input("Target Role *", key="auto_target")
                auto_phone = st.text_input("Phone Number", key="auto_phone")
                auto_linkedin = st.text_input("LinkedIn URL", key="auto_linkedin")
                
            raw_data = st.text_area("Raw Profile Data *", height=200)
            
            if st.button("Initialize Synthesis", type="primary"):
                if auto_name and auto_target and raw_data:
                    st.session_state['target_job'], st.session_state['user_name'] = auto_target, auto_name
                    st.session_state['user_email'], st.session_state['user_phone'] = auto_email, auto_phone
                    st.session_state['user_linkedin'], st.session_state['user_github'] = auto_linkedin, auto_github
                    
                    with st.spinner("Synthesizing..."):
                        prompt = f"Act as an expert Resume Writer. Style: {style}. Target Role: {auto_target}. Raw Data: {raw_data}. RULES: Create a PROFESSIONAL SUMMARY. DO NOT write contact info at the top. Organize into UPPERCASE sections. Return ONLY plain text."
                        st.session_state['resume_text'] = get_gemini_response(prompt)
                        st.success("✅ Synthesis Complete! View output in Tab 2.")
                else: st.error("⚠️ Incomplete Context Parameters.")
        else:
            col_1, col_2 = st.columns(2)
            with col_1:
                man_name = st.text_input("Full Name *", key="man_name")
                man_email = st.text_input("Email Address")
                man_linkedin = st.text_input("LinkedIn Profile URL")
            with col_2:
                man_target = st.text_input("Target Role *", key="man_target")
                man_phone = st.text_input("Phone Number")
                man_github = st.text_input("GitHub URL")
            
            man_summary = st.text_area("Summary (Optional)", height=100)
            man_education = st.text_area("Education Details *")
            man_experience = st.text_area("Work Experience")
            man_skills = st.text_area("Key Skills *")
            man_projects = st.text_area("Major Projects")
            
            if st.button("Initialize Synthesis", type="primary"):
                if man_name and man_target and man_education and man_skills:
                    st.session_state['target_job'], st.session_state['user_name'] = man_target, man_name
                    st.session_state['user_email'], st.session_state['user_phone'] = man_email, man_phone
                    st.session_state['user_linkedin'], st.session_state['user_github'] = man_linkedin, man_github
                    
                    with st.spinner("Synthesizing..."):
                        prompt = f"Act as an expert Resume Writer. Style: {style}. Target Role: {man_target}. Summary: {man_summary}. Education: {man_education}. Experience: {man_experience}. Projects: {man_projects}. Skills: {man_skills}. RULES: Create PROFESSIONAL SUMMARY. DO NOT write contact info at the top. Organize into UPPERCASE sections. Return ONLY plain text."
                        st.session_state['resume_text'] = get_gemini_response(prompt)
                        st.success("✅ Synthesis Complete! View output in Tab 2.")
                else: st.error("⚠️ Incomplete Context Parameters.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        if st.session_state['resume_text']:
            st.markdown("<div class='zna-card'><div style='font-size: 14px; font-weight: 700; color: #3b82f6; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;'><i class='fas fa-magic'></i> Final Review</div>", unsafe_allow_html=True)
            st.session_state['resume_text'] = st.text_area("Edit Generated Document:", value=st.session_state['resume_text'], height=450)
            pdf_data = create_professional_pdf(st.session_state['resume_text'], title=st.session_state['user_name'], email=st.session_state['user_email'], phone=st.session_state['user_phone'], linkedin=st.session_state['user_linkedin'], github=st.session_state['user_github'])
            st.download_button("📥 Export PDF Document", data=pdf_data, file_name=f"Resume_{st.session_state['user_name'].replace(' ', '_')}.pdf", mime="application/pdf", type="primary")
            st.markdown("</div>", unsafe_allow_html=True)
        else: st.warning("👈 Provide context parameters in Tab 1 to initiate synthesis.")

elif app_mode == "✉️ Letter Engine":
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: #0f172a; border: 1px solid #1e293b; padding: 12px; border-radius: 12px;'><i class='fas fa-envelope-open-text' style='color: #8b5cf6; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>Letter Generator</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>Hyper-targeted professional narratives powered by AI.</p>", unsafe_allow_html=True)

    if not st.session_state['resume_text']:
        st.error("⚠️ Missing Profile Context! Synthesize a resume first.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='zna-card'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>JOB TARGET DETAILS</div>", unsafe_allow_html=True)
            company = st.text_input("Target Entity *", placeholder="e.g. Apple, Google")
            hiring_manager = st.text_input("Hiring Lead (Optional)", placeholder="e.g. Design Team")
            job_desc_context = st.text_area("Job Highlights / JD:", height=100)
            
            if st.button("✨ Generate Narratives", type="primary"):
                if company:
                    with st.spinner("Drafting narrative..."):
                        prompt = f"Write cover letter. Target Role: {st.session_state['target_job']}. Company: {company}. Manager: {hiring_manager}. JD Context: {job_desc_context}. Candidate Resume: {st.session_state['resume_text']}. Max 300 words. Plain text."
                        st.session_state['cover_letter_output'] = get_gemini_response(prompt)
                else: st.error("⚠️ Missing Target Entity.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='zna-card' style='height: 100%;'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>DRAFTED OUTPUT</div>", unsafe_allow_html=True)
            if 'cover_letter_output' in st.session_state:
                letter_output = st.session_state['cover_letter_output']
                st.text_area("", value=letter_output, height=250, label_visibility="collapsed")
                pdf_letter = create_professional_pdf(letter_output, title=f"Cover Letter - {st.session_state['user_name']}", email=st.session_state['user_email'], phone=st.session_state['user_phone'], linkedin=st.session_state['user_linkedin'], github=st.session_state['user_github'])
                st.download_button("📥 Export PDF", data=pdf_letter, file_name=f"CoverLetter_{company}.pdf", mime="application/pdf", type="primary")
            else:
                st.markdown("<div style='text-align: center; color: #30363d; margin-top: 60px;'><i class='fas fa-cog fa-3x fa-spin' style='margin-bottom: 20px;'></i><div style='font-size: 14px; font-weight: 700; letter-spacing: 2px;'>AWAITING COMMAND...</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif app_mode == "🔍 ATS Scanner":
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); padding: 12px; border-radius: 12px;'><i class='fas fa-shield-alt' style='color: #22c55e; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>ATS Match Engine</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>Semantic comparison with high-resolution score metrics.</p>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<div class='zna-card'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; display: flex; justify-content: space-between;'>ACTIVE PROFILE <span style='background: rgba(34, 197, 94, 0.1); color: #22c55e; padding: 2px 6px; border-radius: 4px;'>VALIDATED</span></div>", unsafe_allow_html=True)
        if st.session_state['resume_text']:
            st.text_area("", value=st.session_state['resume_text'][:200] + "...\n[Full resume loaded]", height=120, disabled=True, label_visibility="collapsed")
            st.markdown("<div style='border-top: 1px solid #1e293b; margin-top: 15px; padding-top: 15px; font-size: 11px; color: #64748b;'><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>EXPERIENCE NODES <span style='color: #e2e8f0; font-weight: bold;'>✔</span></div><div style='display: flex; justify-content: space-between;'>SKILL CLUSTERS <span style='color: #e2e8f0; font-weight: bold;'>✔</span></div></div>", unsafe_allow_html=True)
        else:
            st.error("⚠️ No Profile Context Loaded.")
        st.markdown("</div>", unsafe_allow_html=True)
            
    with col_r:
        st.markdown("<div class='zna-card' style='height: 100%;'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>TARGET JOB DESCRIPTION</div>", unsafe_allow_html=True)
        job_desc = st.text_area("", height=150, placeholder="Paste Target JD...", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚀 Initiate Deep Scan", type="primary"):
        if st.session_state['resume_text'] and job_desc:
            with st.spinner("Analyzing semantic vectors..."):
                prompt = f"Act as an Applicant Tracking System. Resume: {st.session_state['resume_text']}. JD: {job_desc}. Output: 1. Match Score (%) 2. Missing Keywords 3. Recommendation."
                st.info(get_gemini_response(prompt))
        else: st.warning("⚠️ Parameters missing.")

elif app_mode == "🎙️ Interview Prep":
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: #0f172a; border: 1px solid #1e293b; padding: 12px; border-radius: 12px;'><i class='fas fa-microphone-alt' style='color: #f59e0b; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>Interview Simulator</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>AI-generated questions and strategies based on your exact profile.</p>", unsafe_allow_html=True)

    if not st.session_state['resume_text']:
        st.error("⚠️ Missing Profile Context! Please build your resume in the 'Resume Builder' tab first so the AI knows your background.")
    else:
        col1, col2 = st.columns([0.4, 0.6])
        with col1:
            st.markdown("<div class='zna-card'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>INTERVIEW CONTEXT</div>", unsafe_allow_html=True)
            interview_company = st.text_input("Target Company (Optional)", placeholder="e.g. Amazon, Google, Startup")
            interview_type = st.selectbox("Interview Stage", ["HR Phone Screen", "Technical / Hard Skills", "Behavioral / Cultural Fit", "Executive / Final Round"])
            
            if st.button("🎙️ Generate Mock Interview", type="primary"):
                with st.spinner("Analyzing profile for probable questions..."):
                    prompt = f"""
                    Act as an Expert Technical Recruiter and Hiring Manager conducting a {interview_type} interview for the role of {st.session_state['target_job']} at {interview_company if interview_company else 'a top tech company'}.
                    
                    Candidate's Resume Data:
                    {st.session_state['resume_text']}
                    
                    Based EXACTLY on the specific projects, skills, and experience listed in this resume, generate the top 5 most highly probable interview questions they will be asked.
                    
                    For each question:
                    1. State the Question clearly.
                    2. Provide a "Strategy": Tell the candidate exactly which part of their resume they should highlight to answer it effectively using the STAR method.
                    
                    Keep the formatting clean, professional, and directly actionable.
                    """
                    st.session_state['interview_prep_output'] = get_gemini_response(prompt)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='zna-card' style='height: 100%; min-height: 400px;'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>AI INTERVIEW BLUEPRINT</div>", unsafe_allow_html=True)
            if 'interview_prep_output' in st.session_state:
                st.text_area("", value=st.session_state['interview_prep_output'], height=450, label_visibility="collapsed")
                
                prep_pdf = create_professional_pdf(st.session_state['interview_prep_output'], title=f"Interview Prep - {st.session_state['user_name']}")
                st.download_button("📥 Download Prep Sheet (PDF)", data=prep_pdf, file_name=f"Interview_Prep_{st.session_state['user_name'].replace(' ', '_')}.pdf", mime="application/pdf", type="primary")
            else:
                st.markdown("<div style='text-align: center; color: #30363d; margin-top: 100px;'><i class='fas fa-user-tie fa-3x' style='margin-bottom: 20px;'></i><div style='font-size: 14px; font-weight: 700; letter-spacing: 2px;'>READY TO PREPARE...</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif app_mode == "🗺️ Skill Gap Analyzer":
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: #0f172a; border: 1px solid #1e293b; padding: 12px; border-radius: 12px;'><i class='fas fa-map-marked-alt' style='color: #10b981; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>Skill Gap & Roadmap</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>Discover what's missing and get a custom 4-week learning plan.</p>", unsafe_allow_html=True)

    if not st.session_state['resume_text']:
        st.error("⚠️ Missing Profile Context! Please build your resume in the 'Resume Builder' tab first.")
    else:
        col1, col2 = st.columns([0.4, 0.6])
        with col1:
            st.markdown("<div class='zna-card'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>TARGET DESTINATION</div>", unsafe_allow_html=True)
            dream_job = st.text_input("Your Dream Job / Next Role *", placeholder="e.g. Senior Data Scientist, Product Manager")
            
            if st.button("🗺️ Generate Learning Roadmap", type="primary"):
                if dream_job:
                    with st.spinner(f"Analyzing gap for {dream_job}..."):
                        prompt = f"""
                        Act as an Expert Career Coach and Technical Mentor.
                        
                        Candidate's Current Resume:
                        {st.session_state['resume_text']}
                        
                        Target Dream Job: {dream_job}
                        
                        Please provide:
                        1. MISSING SKILLS: Identify the top 3-5 crucial skills (technical or soft) required for the dream job that are currently missing or weak in the resume.
                        2. 4-WEEK ROADMAP: Create a realistic, structured 4-week learning roadmap to help the candidate acquire these specific missing skills. Include actionable weekly goals or project ideas.
                        
                        Format cleanly with plain text and bullet points. Do not use markdown code blocks.
                        """
                        st.session_state['roadmap_output'] = get_gemini_response(prompt)
                else:
                    st.error("⚠️ Please enter your Target Dream Job.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='zna-card' style='height: 100%; min-height: 400px;'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>CUSTOM ROADMAP</div>", unsafe_allow_html=True)
            if 'roadmap_output' in st.session_state:
                st.text_area("", value=st.session_state['roadmap_output'], height=450, label_visibility="collapsed")
                
                roadmap_pdf = create_professional_pdf(st.session_state['roadmap_output'], title=f"Learning Roadmap - {st.session_state['user_name']}")
                st.download_button("📥 Download Roadmap (PDF)", data=roadmap_pdf, file_name=f"Roadmap_{st.session_state['user_name'].replace(' ', '_')}.pdf", mime="application/pdf", type="primary")
            else:
                st.markdown("<div style='text-align: center; color: #30363d; margin-top: 100px;'><i class='fas fa-compass fa-3x' style='margin-bottom: 20px;'></i><div style='font-size: 14px; font-weight: 700; letter-spacing: 2px;'>AWAITING DESTINATION...</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
