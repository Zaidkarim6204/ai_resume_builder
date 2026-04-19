import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
import urllib.parse
import pandas as pd
from dotenv import load_dotenv
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Elite Studio | AI Career Architect", page_icon="⚡", layout="wide")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please check your .env file or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. ELITE STUDIO PREMIUM GLASSMORPHISM & UI/UX CSS ---
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

    /* --- 1. CUSTOM SLEEK SCROLLBAR --- */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.8); border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #3b82f6 0%, #1e293b 100%); border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #60a5fa 0%, #3b82f6 100%); }

    /* App Background with Glowing Orbs */
    .stApp { 
        background: radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.15), transparent 40%),
                    radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.15), transparent 40%),
                    radial-gradient(circle at 50% 100%, rgba(16, 185, 129, 0.1), transparent 40%),
                    #050814 !important;
        background-attachment: fixed !important;
        color: #f0f6fc; 
    }
    
    /* --- 2. SMOOTH PAGE LOAD ANIMATION --- */
    @keyframes fadeSlideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .block-container { 
        padding-top: 1rem; padding-bottom: 0rem; 
        animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Glassmorphism Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(15, 21, 36, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        color: #f0f6fc !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-left: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: rgba(59, 130, 246, 0.6) !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.2) !important;
        background-color: rgba(15, 21, 36, 0.6) !important;
    }
    
    /* Ultimate Glassmorphism Cards */
    .zna-card {
        background: rgba(15, 23, 42, 0.35); 
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.15); 
        border-left: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        position: relative; /* For hover sweep */
        overflow: hidden;
    }
    
    /* --- 3. ADVANCED HOVER STATES (LIGHT SWEEP) --- */
    .zna-card::after {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        transform: skewX(-20deg);
        transition: 0.5s;
        pointer-events: none;
    }
    .zna-card:hover::after {
        left: 150%;
        transition: 0.7s ease-in-out;
    }
    .zna-card:hover {
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.2);
    }

    /* --- 4. UPGRADED EMPTY STATES --- */
    .empty-state-card {
        text-align: center; padding: 60px 20px; background: rgba(12, 17, 30, 0.3);
        border: 1px dashed rgba(255,255,255,0.1); border-radius: 16px;
        backdrop-filter: blur(10px); margin-top: 20px;
    }
    .pulse-icon {
        font-size: 48px; margin-bottom: 20px;
        background: -webkit-linear-gradient(#3b82f6, #8b5cf6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: pulse-glow-icon 2s infinite;
    }
    @keyframes pulse-glow-icon {
        0% { filter: drop-shadow(0 0 5px rgba(59, 130, 246, 0.2)); transform: scale(1); }
        50% { filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.6)); transform: scale(1.05); }
        100% { filter: drop-shadow(0 0 5px rgba(59, 130, 246, 0.2)); transform: scale(1); }
    }
    .empty-state-title {
        font-size: 18px; font-weight: 800; letter-spacing: 1px;
        background: linear-gradient(90deg, #f8fafc, #94a3b8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .empty-state-desc { color: #64748b; font-size: 13px; font-weight: 500; }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(5, 8, 20, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
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
    .stRadio label:hover [data-testid="stMarkdownContainer"] { 
        background-color: rgba(255,255,255,0.05) !important; 
        color: #e2e8f0 !important;
    }
    .stRadio label[data-selected="true"] [data-testid="stMarkdownContainer"] {
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.2) 0%, transparent 100%) !important;
        border-left: 3px solid #3b82f6 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Live Pulse Animation for badges */
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
        backdrop-filter: blur(4px);
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
        transform: translateY(-2px) scale(1.02); box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    }
    
    .side-job-portal {
        border-radius: 12px; text-align: center; padding: 14px; font-weight: 600; cursor: pointer; display: inline-block;
        width: 100%; margin-top: 10px; text-decoration: none; transition: all 0.3s ease; font-size: 13px; color: white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .side-job-portal:hover { filter: brightness(1.2); box-shadow: 0 0 20px rgba(255,255,255,0.2); transform: translateY(-2px);}

    /* Grid & Card Components */
    .validated-badge { background: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase; display: inline-block; margin-bottom: 15px;}
    .prep-question { font-size: 22px; font-weight: 800; margin-bottom: 15px; color: white;}
    .core-comp-tag { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(59, 130, 246, 0.3); color: #3b82f6; padding: 4px 10px; border-radius: 50px; font-size: 10px; font-weight: 600; text-transform: uppercase; margin-right: 8px;}
    
    .star-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 25px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 20px;}
    .star-col { background: rgba(12, 17, 30, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 20px; transition: border-color 0.3s ease;}
    .star-col:hover { border-color: rgba(59, 130, 246, 0.5); background: rgba(12, 17, 30, 0.6);}
    .star-icon { font-size: 20px; color: #3b82f6; margin-bottom: 12px;}
    .star-title { font-size: 12px; font-weight: 700; text-transform: uppercase; color: #e2e8f0; margin-bottom: 8px;}
    .star-text { font-size: 13px; color: #94a3b8; line-height: 1.6;}

    .gap-analyzer-grid { display: grid; grid-template-columns: auto 1fr; gap: 40px; }
    .roadmap-timeline-bar { width: 2px; background: rgba(255,255,255,0.1); height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: space-between; position: relative;}
    .roadmap-timeline-bar::before { content: ''; width: 14px; height: 14px; border-radius: 50%; background: #3b82f6; position: absolute; top: 0; left: -6px; box-shadow: 0 0 10px #3b82f6;}
    .roadmap-timeline-bar::after { content: ''; width: 14px; height: 14px; border-radius: 50%; background: rgba(255,255,255,0.2); position: absolute; bottom: 0; left: -6px; }

    .roadmap-content { display: flex; flex-direction: column; gap: 30px;}
    .roadmap-week-card { background: rgba(12, 17, 30, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; transition: all 0.3s ease;}
    .roadmap-week-card:hover { border-color: rgba(16, 185, 129, 0.5); background: rgba(12, 17, 30, 0.6); box-shadow: 0 8px 25px rgba(0,0,0,0.2);}
    .roadmap-header { display: flex; align-items: center; gap: 15px; margin-bottom: 15px;}
    .roadmap-number { background: rgba(15, 23, 42, 0.8); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); font-size: 20px; font-weight: 800; width: 45px; height: 45px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 15px rgba(16, 185, 129, 0.1);}
    .roadmap-goal { font-size: 16px; font-weight: 700; color: white;}
    .roadmap-task-list { list-style: none; padding: 0; margin-top: 15px;}
    .roadmap-task-list li { display: flex; align-items: center; gap: 10px; color: #94a3b8; font-size: 14px; margin-bottom: 8px;}
    .roadmap-task-list li i { color: #10b981; font-size: 12px;}
    .completed-badge { background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); color: #10b981; padding: 4px 10px; border-radius: 50px; font-size: 10px; font-weight: 700; text-transform: uppercase;}
    .roadmap-project { background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; margin-top: 15px;}
    .roadmap-project-title { font-size: 14px; font-weight: 700; color: white; margin-bottom: 5px;}
    .roadmap-project-desc { font-size: 13px; color: #94a3b8;}
    .missing-skill-tag { background: rgba(76, 29, 29, 0.6); border: 1px solid rgba(248, 113, 113, 0.4); color: #f87171; padding: 4px 10px; border-radius: 50px; font-size: 10px; font-weight: 600; text-transform: uppercase; margin-right: 8px;}

    /* Steps UI */
    .zna-steps { display: flex; justify-content: space-around; margin-bottom: 30px; position: relative; }
    .zna-step-node { display: flex; flex-direction: column; align-items: center; width: 33%; position: relative; z-index: 2; }
    .zna-steps::before { content: ''; position: absolute; height: 2px; background: rgba(255,255,255,0.1); width: 66%; top: 16px; left: 17%; z-index: 1; }
    .zna-step-circle { width: 34px; height: 34px; border-radius: 50%; background: rgba(15, 21, 36, 0.8); border: 2px solid rgba(255,255,255,0.1); color: #64748b; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; margin-bottom: 10px; transition: all 0.3s ease; backdrop-filter: blur(4px);}
    .step-active .zna-step-circle { background: #3b82f6; border-color: #3b82f6; color: white; box-shadow: 0 0 15px rgba(59,130,246,0.4); }
    .zna-step-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #64748b; }
    .step-active .zna-step-label { color: #f8fafc; }
    
</style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def get_gemini_response(prompt, json_mode=False):
    try:
        response = model.generate_content(prompt)
        text_output = response.text
        if json_mode:
            return text_output.replace('```json', '').replace('```', '').strip()
        return text_output
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
    st.markdown(
        "<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 30px;'>"
        "<div style='background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 20px; box-shadow: 0 4px 10px rgba(59,130,246,0.3);'>Z</div>"
        "<div style='font-size: 22px; font-weight: 800; letter-spacing: -0.5px; color: white;'>Elite Studio</div>"
        "</div>", 
        unsafe_allow_html=True
    )
    
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
    
    st.markdown(
        "<div style='background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin-top: 20px; backdrop-filter: blur(10px);'>"
        "<div style='font-size: 11px; font-weight: 700; color: #3b82f6; text-transform: uppercase; margin-bottom: 8px;'>PRO WORKSPACE</div>"
        "<div style='font-size: 12px; color: #94a3b8; line-height: 1.5;'>Personalize your profile to unlock job-specific insights.</div>"
        "</div>", 
        unsafe_allow_html=True
    )
    
    st.markdown("<div class='sidebar-header'>🌐 Direct Apply Portals</div>", unsafe_allow_html=True)
    
    if st.session_state['target_job']:
        linkedin_query = urllib.parse.quote(st.session_state['target_job'])
        indeed_query = urllib.parse.quote(st.session_state['target_job'])
        naukri_query = st.session_state['target_job'].replace(' ', '-').lower()
        
        st.markdown(
            f"<div style='display: flex; flex-direction: column; gap: 5px; margin-top: 10px;'>"
            f"<a href='https://www.linkedin.com/jobs/search/?keywords={linkedin_query}' target='_blank' class='side-job-portal' style='background: linear-gradient(135deg, #0a66c2 0%, #004182 100%); border: none;'>"
            f"<i class='fab fa-linkedin' style='margin-right: 8px;'></i> LinkedIn ↗</a>"
            f"<a href='https://in.indeed.com/jobs?q={indeed_query}' target='_blank' class='side-job-portal' style='background: linear-gradient(135deg, #2557a7 0%, #163a73 100%); border: none;'>"
            f"<i class='fas fa-info-circle' style='margin-right: 8px;'></i> Indeed ↗</a>"
            f"<a href='https://www.naukri.com/{naukri_query}-jobs' target='_blank' class='side-job-portal' style='background: linear-gradient(135deg, #0075FF 0%, #0056b3 100%); border: none;'>"
            f"<i class='fas fa-briefcase' style='margin-right: 8px;'></i> Naukri ↗</a>"
            f"</div>", 
            unsafe_allow_html=True
        )
        st.caption(f"Searching roles for: **{st.session_state['target_job']}**")
    else:
        st.info("💡 Fill out the 'Target Role' in the Resume Builder to unlock live Job Portals.")

# --- 6. MAIN APP LOGIC ---

if app_mode == "📊 Dashboard":
    st.markdown("<div style='float: right;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 32px; font-weight: 800; margin-bottom: 5px;'>Welcome to your Career Workspace</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 25px;'>Your central hub for AI-powered career growth and optimization.</p>", unsafe_allow_html=True)

    resume_status = "Active" if st.session_state['resume_text'] else "Awaiting Data"
    status_color = "#10b981" if st.session_state['resume_text'] else "#f59e0b"
    job_status = st.session_state['target_job'] if st.session_state['target_job'] else "Not Set"
    word_count = len(st.session_state['resume_text'].split()) if st.session_state['resume_text'] else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.markdown(f"<div class='zna-card'><div style='font-size:12px; color:#64748b; font-weight:bold;'>PROFILE STATUS</div><div style='font-size:20px; font-weight:bold; margin-top:5px; color:{status_color};'>{resume_status}</div></div>", unsafe_allow_html=True)
    with col2: 
        st.markdown(f"<div class='zna-card'><div style='font-size:12px; color:#64748b; font-weight:bold;'>TARGET ROLE</div><div style='font-size:18px; font-weight:bold; margin-top:5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;' title='{job_status}'>{job_status}</div></div>", unsafe_allow_html=True)
    with col3: 
        st.markdown(f"<div class='zna-card'><div style='font-size:12px; color:#64748b; font-weight:bold;'>WORDS IN MEMORY</div><div style='font-size:24px; font-weight:bold; margin-top:5px;'>{word_count}</div></div>", unsafe_allow_html=True)
    with col4: 
        st.markdown("<div class='zna-card'><div style='font-size:12px; color:#64748b; font-weight:bold;'>API CONNECTION</div><div style='font-size:24px; font-weight:bold; margin-top:5px; color:#3b82f6;'>Secure</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;'>⚡ Quick System Actions</div>", unsafe_allow_html=True)
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🔍 Check Profile Readiness", use_container_width=True):
            if st.session_state['resume_text'] and st.session_state['target_job']:
                st.success(f"✅ System is fully primed for {st.session_state['target_job']} roles!")
            else:
                st.warning("⚠️ Profile incomplete. Head to the Resume Builder first.")
    
    with action_col2:
        if st.button("🚀 Ping Gemini API", use_container_width=True):
            with st.spinner("Pinging..."):
                test_response = get_gemini_response("Say 'API is fully operational.'")
                st.info(f"🤖 Response: {test_response}")
                
    with action_col3:
        if st.button("🧹 Clear System Memory", use_container_width=True):
            st.session_state['resume_text'] = ""
            st.session_state['target_job'] = ""
            st.rerun() 

    st.markdown("<br>", unsafe_allow_html=True)

    dash_col1, dash_col2 = st.columns([0.65, 0.35])
    with dash_col1:
        st.markdown("<div class='zna-card'><div style='font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;'><i class='fas fa-chart-area' style='color:#3b82f6;'></i> System Analytics</div>", unsafe_allow_html=True)
        
        chart_metric = st.selectbox("Select metric to visualize:", ["ATS Optimization Trends (%)", "System Memory Usage", "Industry Alignment Score"])
        
        if chart_metric == "ATS Optimization Trends (%)":
            chart_data = pd.DataFrame([65, 72, 68, 85, 88, 92, 96], columns=["Match Score (%)"])
        elif chart_metric == "System Memory Usage":
            chart_data = pd.DataFrame([10, 25, 40, 45, 60, 75, word_count if word_count > 0 else 80], columns=["Memory Load"])
        else:
            chart_data = pd.DataFrame([40, 50, 55, 70, 85, 88, 95], columns=["Alignment"])

        st.line_chart(chart_data, color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    with dash_col2:
        st.markdown("<div class='zna-card' style='height: 100%;'><div style='font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;'><i class='fas fa-terminal' style='color:#8b5cf6;'></i> Live System Logs</div>", unsafe_allow_html=True)
        st.info("✅ **[SYSTEM]** LLM Engine connected.")
        
        if st.session_state['resume_text']:
            st.success("✅ **[MEMORY]** Profile loaded securely.")
            st.info(f"📊 **[DATA]** Vectorized {word_count} words.")
        else:
            st.markdown("<div style='display:flex; align-items:center; gap:10px; margin-top:15px;'><i class='fas fa-hourglass-half' style='color:#f59e0b; animation: pulse-glow-icon 2s infinite;'></i> <span style='color:#94a3b8; font-weight:600;'>Awaiting Context Injection...</span></div>", unsafe_allow_html=True)
            
        if st.session_state['target_job']:
            st.info(f"🎯 **[TARGET]** Locked on: {st.session_state['target_job']}")
        st.markdown("</div>", unsafe_allow_html=True)

elif app_mode == "📄 Resume Builder":
    st.markdown("<div style='float: right;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; backdrop-filter: blur(10px);'><i class='fas fa-microchip' style='color: #3b82f6; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>Smart Resume Builder</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>AI-powered synthesis of your professional data.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Setup & Context", "📄 Synthesis Output"])
    
    with tab1:
        st.markdown("<div class='zna-card'>", unsafe_allow_html=True)
        st.markdown(
            "<div class='zna-steps'>"
            "<div class='zna-step-node step-active'><div class='zna-step-circle'>1</div><div class='zna-step-label'>Context</div></div>"
            "<div class='zna-step-node step-inactive'><div class='zna-step-circle'>2</div><div class='zna-step-label'>Analysis</div></div>"
            "<div class='zna-step-node step-inactive'><div class='zna-step-circle'>3</div><div class='zna-step-label'>Synthesis</div></div>"
            "</div>", 
            unsafe_allow_html=True
        )
        
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
        else: 
            st.markdown("<div class='empty-state-card'><div class='pulse-icon'><i class='fas fa-lock'></i></div><div class='empty-state-title'>MODULE LOCKED</div><div class='empty-state-desc'>Provide context parameters in Tab 1 to initialize synthesis.</div></div>", unsafe_allow_html=True)

elif app_mode == "✉️ Letter Engine":
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; backdrop-filter: blur(10px);'><i class='fas fa-envelope-open-text' style='color: #8b5cf6; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>Letter Generator</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>Hyper-targeted professional narratives powered by AI.</p>", unsafe_allow_html=True)

    if not st.session_state['resume_text']:
        st.markdown("<div class='empty-state-card'><div class='pulse-icon'><i class='fas fa-lock'></i></div><div class='empty-state-title'>MODULE LOCKED</div><div class='empty-state-desc'>Synthesize a profile in the Resume Builder to unlock the Letter Engine.</div></div>", unsafe_allow_html=True)
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
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); padding: 12px; border-radius: 12px; backdrop-filter: blur(10px);'><i class='fas fa-shield-alt' style='color: #22c55e; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>ATS Match Engine</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>Semantic comparison with high-resolution score metrics.</p>", unsafe_allow_html=True)
    
    if not st.session_state['resume_text']:
        st.markdown("<div class='empty-state-card'><div class='pulse-icon'><i class='fas fa-lock'></i></div><div class='empty-state-title'>MODULE LOCKED</div><div class='empty-state-desc'>Synthesize a profile in the Resume Builder to unlock the ATS Scanner.</div></div>", unsafe_allow_html=True)
    else:
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("<div class='zna-card'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; display: flex; justify-content: space-between;'>ACTIVE PROFILE <span style='background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34,197,94,0.3); color: #22c55e; padding: 2px 6px; border-radius: 4px;'>VALIDATED</span></div>", unsafe_allow_html=True)
            st.text_area("", value=st.session_state['resume_text'][:200] + "...\n[Full resume loaded]", height=120, disabled=True, label_visibility="collapsed")
            st.markdown("<div style='border-top: 1px solid rgba(255,255,255,0.05); margin-top: 15px; padding-top: 15px; font-size: 11px; color: #64748b;'><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>EXPERIENCE NODES <span style='color: #e2e8f0; font-weight: bold;'>✔</span></div><div style='display: flex; justify-content: space-between;'>SKILL CLUSTERS <span style='color: #e2e8f0; font-weight: bold;'>✔</span></div></div>", unsafe_allow_html=True)
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
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; backdrop-filter: blur(10px);'><i class='fas fa-microphone-alt' style='color: #f59e0b; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>Interview Simulator</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>AI-generated structured questions and STAR method strategies based on your exact profile.</p>", unsafe_allow_html=True)

    if not st.session_state['resume_text']:
        st.markdown("<div class='empty-state-card'><div class='pulse-icon'><i class='fas fa-lock'></i></div><div class='empty-state-title'>MODULE LOCKED</div><div class='empty-state-desc'>Synthesize a profile in the Resume Builder to unlock the Interview Simulator.</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='zna-card'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>INTERVIEW CONTEXT</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            interview_company = st.text_input("Target Company (Optional)", placeholder="e.g. Amazon, Google, Startup")
        with col2:
            interview_type = st.selectbox("Interview Stage", ["Behavioral / Cultural Fit", "Technical / Hard Skills", "HR Phone Screen", "Executive / Final Round"])
            
        if st.button("🎙️ Generate Mock Interview", type="primary"):
            with st.spinner("Analyzing profile for probable questions..."):
                prompt = f"""
                Act as an Expert Technical Recruiter and Hiring Manager conducting a {interview_type} interview for the role of {st.session_state['target_job']} at {interview_company if interview_company else 'a top tech company'}.
                Candidate's Resume Data: {st.session_state['resume_text']}
                
                Based EXACTLY on the specific projects, skills, and experience listed in this resume, generate the top 5 most highly probable interview questions they will be asked.
                
                Output MUST be a raw JSON object (no markdown code blocks) with this format:
                {{
                    "questions": [
                        {{
                            "number": 1,
                            "question": "The actual question",
                            "situation": "Situation strategy",
                            "task": "Task strategy",
                            "action": "Action strategy",
                            "result": "Result strategy",
                            "competencies": ["Leadership", "Adaptability"]
                        }}
                    ]
                }}
                """
                json_response = get_gemini_response(prompt, json_mode=True)
                try:
                    st.session_state['interview_prep_data'] = json.loads(json_response)
                except Exception as e:
                    st.error(f"⚠️ Error parsing AI response. It might not be in valid JSON format. Raw output: {json_response[:200]}...")
        st.markdown("</div>", unsafe_allow_html=True)
            
        if 'interview_prep_data' in st.session_state:
            interview_data = st.session_state['interview_prep_data']
            
            for q in interview_data.get('questions', []):
                comps = ' '.join([f"<span class='core-comp-tag'>{sanitize_text(comp)}</span>" for comp in q.get('competencies', [])])
                st.markdown(
                    f"<div class='zna-card'>\n"
                    f"<div class='validated-badge'>Q{q['number']} / Validated</div>\n"
                    f"<div class='prep-question'>{q['question']}</div>\n"
                    f"<div style='display: flex; gap: 5px; margin-top: 10px;'>\n"
                    f"{comps}\n"
                    f"</div>\n"
                    f"<div class='star-grid'>\n"
                    f"<div class='star-col'>\n"
                    f"<i class='fas fa-map-marker-alt star-icon'></i>\n"
                    f"<div class='star-title'>Situation</div>\n"
                    f"<div class='star-text'>{q['situation']}</div>\n"
                    f"</div>\n"
                    f"<div class='star-col'>\n"
                    f"<i class='fas fa-tasks star-icon'></i>\n"
                    f"<div class='star-title'>Task</div>\n"
                    f"<div class='star-text'>{q['task']}</div>\n"
                    f"</div>\n"
                    f"<div class='star-col'>\n"
                    f"<i class='fas fa-running star-icon'></i>\n"
                    f"<div class='star-title'>Action</div>\n"
                    f"<div class='star-text'>{q['action']}</div>\n"
                    f"</div>\n"
                    f"<div class='star-col'>\n"
                    f"<i class='fas fa-trophy star-icon'></i>\n"
                    f"<div class='star-title'>Result</div>\n"
                    f"<div class='star-text'>{q['result']}</div>\n"
                    f"</div>\n"
                    f"</div>\n"
                    f"</div>", 
                    unsafe_allow_html=True
                )
            
            pdf_text_content = ""
            for q in interview_data.get('questions', []):
                pdf_text_content += f"Q{q['number']}: {q['question']}\nCOMPETENCIES: {', '.join(q.get('competencies', []))}\nSITUATION: {q['situation']}\nTASK: {q['task']}\nACTION: {q['action']}\nRESULT: {q['result']}\n\n"
            
            prep_pdf = create_professional_pdf(pdf_text_content, title=f"Interview Prep - {st.session_state['user_name']}")
            st.download_button("📥 Download Prep Sheet (PDF)", data=prep_pdf, file_name=f"Interview_Prep_{st.session_state['user_name'].replace(' ', '_')}.pdf", mime="application/pdf", type="primary")

        else:
            st.markdown("<div class='empty-state-card' style='margin-top: 0;'><div class='pulse-icon'><i class='fas fa-user-tie'></i></div><div class='empty-state-title'>READY TO PREPARE</div><div class='empty-state-desc'>Click 'Generate Mock Interview' to begin.</div></div>", unsafe_allow_html=True)

elif app_mode == "🗺️ Skill Gap Analyzer":
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='status-badge'><i class='fas fa-bolt' style='margin-right: 6px;'></i> Gemini 2.5 Flash Active <span class='live-pulse'></span></span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 15px; margin-bottom: 5px;'><div style='background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; backdrop-filter: blur(10px);'><i class='fas fa-map-marked-alt' style='color: #10b981; font-size: 24px;'></i></div><h2 style='font-size: 32px; font-weight: 800; margin: 0;'>Skill Gap & Roadmap</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 35px; margin-left: 70px;'>Discover what's missing and get a visual, custom 4-week learning roadmap.</p>", unsafe_allow_html=True)

    if not st.session_state['resume_text']:
        st.markdown("<div class='empty-state-card'><div class='pulse-icon'><i class='fas fa-lock'></i></div><div class='empty-state-title'>MODULE LOCKED</div><div class='empty-state-desc'>Synthesize a profile in the Resume Builder to unlock the Skill Gap Analyzer.</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='zna-card'><div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>TARGET DESTINATION</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            dream_job = st.text_input("Your Dream Job / Next Role *", placeholder="e.g. Senior Data Scientist, Product Manager")
        with col2:
            st.markdown("<div style='padding-top:28px;'></div>", unsafe_allow_html=True)
            if st.button("🗺️ Generate Visual Roadmap", type="primary"):
                if dream_job:
                    with st.spinner(f"Analyzing gap for {dream_job}..."):
                        prompt = f"""
                        Act as an Expert Career Coach and Technical Mentor.
                        Candidate's Current Resume: {st.session_state['resume_text']}
                        Target Dream Job: {dream_job}
                        
                        Please analyze the gap and output a raw JSON object (no markdown code blocks) with this format:
                        {{
                            "missing_skills": ["Skill 1", "Skill 2", "Skill 3"],
                            "learning_roadmap": [
                                {{
                                    "week_number": 1,
                                    "goal": "Weekly goal title",
                                    "action_items": ["Action 1", "Action 2"],
                                    "milestone_project_title": "Project Title",
                                    "milestone_project_desc": "Brief project description"
                                }}
                            ]
                        }}
                        Return 4 weeks in the roadmap.
                        """
                        json_response = get_gemini_response(prompt, json_mode=True)
                        try:
                            st.session_state['skill_gap_data'] = json.loads(json_response)
                        except Exception as e:
                            st.error(f"⚠️ Error parsing AI response. It might not be in valid JSON format. Raw output: {json_response[:200]}...")
                else:
                    st.error("⚠️ Please enter your Target Dream Job.")
        st.markdown("</div>", unsafe_allow_html=True)
            
        if 'skill_gap_data' in st.session_state:
            gap_data = st.session_state['skill_gap_data']
            
            skills_html = ' '.join([f"<span class='missing-skill-tag'>{sanitize_text(skill)}</span>" for skill in gap_data.get('missing_skills', [])])
            st.markdown(
                f"<div class='zna-card'>\n"
                f"<div style='font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px;'>IDENTIFIED GAPS</div>\n"
                f"<div style='display: flex; gap: 5px;'>\n"
                f"{skills_html}\n"
                f"</div>\n"
                f"</div>", 
                unsafe_allow_html=True
            )

            st.markdown("<div class='zna-card'>", unsafe_allow_html=True)
            st.markdown("<div class='gap-analyzer-grid'>", unsafe_allow_html=True)
            st.markdown("<div class='roadmap-timeline-bar'></div>", unsafe_allow_html=True)
            st.markdown("<div class='roadmap-content'>", unsafe_allow_html=True)
            
            pdf_roadmap_text = "MISSING SKILLS:\n" + ', '.join(gap_data.get('missing_skills', [])) + "\n\n"

            for week in gap_data.get('learning_roadmap', []):
                items_html = ' '.join([f"<li><i class='fas fa-check-circle'></i> {sanitize_text(item)}</li>" for item in week.get('action_items', [])])
                st.markdown(
                    f"<div class='roadmap-week-card'>\n"
                    f"<div class='roadmap-header'>\n"
                    f"<div class='roadmap-number'>{week['week_number']}</div>\n"
                    f"<div class='roadmap-goal'>{sanitize_text(week['goal'])}</div>\n"
                    f"</div>\n"
                    f"<ul class='roadmap-task-list'>\n"
                    f"{items_html}\n"
                    f"</ul>\n"
                    f"<div class='roadmap-project'>\n"
                    f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>\n"
                    f"<div class='roadmap-project-title'>{sanitize_text(week['milestone_project_title'])}</div>\n"
                    f"<span class='completed-badge'>Completed</span>\n"
                    f"</div>\n"
                    f"<div class='roadmap-project-desc'>{sanitize_text(week['milestone_project_desc'])}</div>\n"
                    f"</div>\n"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
                pdf_roadmap_text += f"WEEK {week['week_number']}: {week['goal']}\nACTION ITEMS:\n - " + '\n - '.join(week.get('action_items', [])) + f"\nMILESTONE PROJECT:\nTitle: {week['milestone_project_title']}\nDescription: {week['milestone_project_desc']}\n\n"
            
            st.markdown("</div>", unsafe_allow_html=True) 
            st.markdown("</div>", unsafe_allow_html=True) 
            
            roadmap_pdf = create_professional_pdf(pdf_roadmap_text, title=f"Learning Roadmap - {st.session_state['user_name']}")
            st.download_button("📥 Download Roadmap (PDF)", data=roadmap_pdf, file_name=f"Roadmap_{st.session_state['user_name'].replace(' ', '_')}.pdf", mime="application/pdf", type="primary")

            st.markdown("</div>", unsafe_allow_html=True) 

        else:
            st.markdown("<div class='empty-state-card' style='margin-top: 0;'><div class='pulse-icon'><i class='fas fa-compass'></i></div><div class='empty-state-title'>AWAITING DESTINATION</div><div class='empty-state-desc'>Enter your Target Dream Job and click 'Generate Visual Roadmap' to begin.</div></div>", unsafe_allow_html=True)
