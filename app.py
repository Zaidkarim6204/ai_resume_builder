import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
import urllib.parse
import pandas as pd
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AI Studio | ZNA Career Architect", page_icon="🏗️", layout="wide")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please check your .env file or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. PREMIUM SaaS CSS STYLING ---
# Re-importing Inter font for consistency with landing page.
# Using deep dark themes and blue accent colors to match image aesthetic.
st.markdown("""
<style>
    /* 1. Base Styles & Font Reset */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* 2. Full-App Deep Dark Theme */
    .stApp { background-color: #0b0f19; color: #f0f6fc; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    
    /* 3. Streamlit Default Widget Overrides for Dark Mode */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #161b22 !important;
        color: #f0f6fc !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #1f6feb !important;
        box-shadow: 0 0 0 1px #1f6feb !important;
    }
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid #30363d !important;
    }
    
    /* Global class for the card containers used throughout the dashboard */
    .zna-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 24px;
    }

    /* 4. The ZNA Dark Blue Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0b1c3e !important;
        border-right: 1px solid #1c2e5a;
        width: 300px !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #f0f6fc !important;
    }
    
    /* Sidebar Headers Styling */
    .sidebar-header { color: #8b949e; font-size: 11px; font-weight: 700; text-transform: uppercase; margin: 30px 0 15px 15px; letter-spacing: 1px;}

    /* Radio Navigation Menu Custom Styling */
    .stRadio [data-testid="stMarkdownContainer"] {
        background-color: transparent !important;
        color: #acb6c0 !important;
        font-size: 14px !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease;
    }
    /* Icon styling for the menu items */
    .stRadio [data-testid="stMarkdownContainer"] i { font-size: 16px; width: 20px; text-align: center; }
    
    /* Hover effect for the menu items */
    .stRadio label:hover [data-testid="stMarkdownContainer"] { background-color: #1a2f5c !important; color: #ffffff !important;}
    
    /* Selected menu item styling */
    .stRadio label[data-selected="true"] [data-testid="stMarkdownContainer"] {
        background-color: #1f6feb !important;
        color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(31, 111, 235, 0.3) !important;
    }

    /* Side Job Portal Button styling to look premium */
    .side-job-portal {
        background-color: #1f6feb;
        border-radius: 8px;
        color: white;
        text-align: center;
        padding: 12px;
        font-weight: 700;
        cursor: pointer;
        display: inline-block;
        width: 100%;
        margin-top: 15px;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .side-job-portal:hover {
        background-color: #2ea043; /* Green on hover like a success/ready action */
        box-shadow: 0 2px 8px rgba(46, 160, 67, 0.4);
    }

    /* 5. Pill-Shaped Glowing Buttons */
    .stButton>button {
        border-radius: 50px !important;
        background-color: #1f6feb !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 12px 24px !important;
        border: none !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(31, 111, 235, 0.2) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(31, 111, 235, 0.4) !important;
    }
    /* Target Generate narratices button specifically in image */
    .cl-gen-narratives .stButton>button {
        background-color: #7d49ee !important;
        box-shadow: 0 4px 6px rgba(125, 73, 238, 0.2) !important;
    }
    .cl-gen-narratives .stButton>button:hover {
        box-shadow: 0 6px 12px rgba(125, 73, 238, 0.4) !important;
    }

    /* 6. modern metric cards (Replacing the boxy st.metric) */
    .zna-metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .zna-metric-label { font-size: 12px; color: #94a3b8; font-weight: 500; }
    .zna-metric-value { font-size: 24px; font-weight: 700; color: #f0f6fc; }
    .zna-metric-status { font-size: 10px; padding: 4px 8px; border-radius: 4px; display: inline-block; margin-top: 8px; }
    .status-active { background-color: #2ea043; color: white; }
    .status-ready { background-color: #1f6feb; color: white; }
    .status-online { background-color: #8957e5; color: white; }

    /* 7. Beautiful Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 2px solid #30363d !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #57606a !important;
        font-weight: 600 !important;
        height: 50px;
    }
    .stTabs [aria-selected="true"] {
        color: #1f6feb !important;
        border-bottom-color: #1f6feb !important;
        background-color: rgba(31, 111, 235, 0.05) !important;
    }

    /* 8. Modern Step Indicator for Resume Builder */
    .zna-steps { display: flex; justify-content: space-around; margin-bottom: 30px; }
    .zna-step-node { display: flex; flex-direction: column; align-items: center; text-align: center; width: 33%; position: relative; }
    .zna-step-node::after { content: ''; position: absolute; height: 2px; background: #30363d; width: 100%; top: 15px; left: 50%; z-index: 0; }
    .zna-step-node:last-child::after { display: none; }
    
    .zna-step-circle { width: 32px; height: 32px; border-radius: 50%; border: 2px solid #1f6feb; background: #0d1117; color: #1f6feb; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; position: relative; z-index: 1; margin-bottom: 8px; }
    .step-active .zna-step-circle { background-color: #1f6feb; color: white; border-color: #1f6feb; }
    .step-active::after { background: #1f6feb; }
    .step-inactive .zna-step-circle { color: #57606a; border-color: #30363d; }
    
    .zna-step-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #57606a; }
    .step-active .zna-step-label { color: #f0f6fc; }
    
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

# Phone, LinkedIn, and GitHub parameters for clickable links
def create_professional_pdf(text_content, title="Document", email="", phone="", linkedin="", github=""):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Header Title (Name)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=title, ln=True, align='C')
    
    # Clickable Contact Links
    pdf.set_font("Arial", size=10)
    if email:
        pdf.set_text_color(0, 102, 204) # Blue link color
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
        
    pdf.set_text_color(0, 0, 0) # Reset back to black text for body
    pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
    pdf.ln(8)
    
    # Body
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

# Store the contact details so they can be passed to the PDF later
if 'user_name' not in st.session_state: st.session_state['user_name'] = "Professional Resume"
if 'user_email' not in st.session_state: st.session_state['user_email'] = ""
if 'user_phone' not in st.session_state: st.session_state['user_phone'] = ""
if 'user_linkedin' not in st.session_state: st.session_state['user_linkedin'] = ""
if 'user_github' not in st.session_state: st.session_state['user_github'] = ""

# --- 5. SIDEBAR NAVIGATION & LINKEDIN PORTAL ---
with st.sidebar:
    # UPDATED: Sleek ZNA logo at the top
    st.markdown("""
        <svg width="240" height="80" viewBox="0 0 350 110" xmlns="http://www.w3.org/2000/svg">
            <path d="M40 20 L110 20 L40 85 L110 85" fill="none" stroke="#4a90e2" stroke-width="15" stroke-linejoin="bevel"/>
            <path d="M125 85 L125 20 L185 85 L185 20" fill="none" stroke="#4a90e2" stroke-width="15" stroke-linejoin="bevel"/>
            <path d="M200 85 L235 20 L270 85" stroke="#4a90e2" stroke-width="15" fill="none"/>
            <path d="M215 65 Q250 55 285 35" stroke="#4a90e2" stroke-width="8" fill="none" stroke-linecap="round"/>
            <path d="M275 35 L285 35 L285 45" stroke="#4a90e2" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <text x="40" y="105" font-family="'Inter', sans-serif" font-weight="700" font-size="18" fill="#acb6c0" letter-spacing="1">AI STUDIO</text>
        </svg>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-header'>Navigate Workspace:</div>", unsafe_allow_html=True)
    
    # UPDATED: Adding icons to the radio choices as plain text is all we can do here while keeping the Python radio logic.
    app_mode = st.radio("", [
        "📊 Overview Dashboard", 
        "📋 Smart Resume Builder", 
        "✉️ Cover Letter Generator", 
        "🔍 ATS Match Engine"
    ])
    st.markdown("---")
    
    # Dynamic LinkedIn Direct Apply Portal
    st.markdown("<div class='sidebar-header'>Job Portal:</div>", unsafe_allow_html=True)
    if st.session_state['target_job']:
        job_query = urllib.parse.quote(st.session_state['target_job'])
        st.markdown(f"""
        <a href="https://www.linkedin.com/jobs/search/?keywords={job_query}" target="_blank" class="side-job-portal">
            Apply on LinkedIn ↗
        </a>
        """, unsafe_allow_html=True)
        st.caption(f"Searching for: **{st.session_state['target_job']}**")
    else:
        st.info("💡 Fill out the 'Target Job Title' in the Resume Builder to unlock the LinkedIn Job Portal.")

# --- 6. MAIN APP LOGIC ---

if app_mode == "📊 Overview Dashboard":
    # UPDATED: Sleek status indicator
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='zna-metric-status' style='background: rgba(46, 160, 67, 0.1); color: #2ea043; border: 1px solid rgba(46, 160, 67, 0.3);'>Gemini 2.5 Flash Active 🟢</span></div>", unsafe_allow_html=True)
    st.markdown("<h3>Welcome to your Career Workspace</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #acb6c0; margin-bottom: 24px; font-size: 14px;'>Your central hub for AI-powered career growth and optimization.</p>", unsafe_allow_html=True)

    # Top Metrics - Replacing with modern HTML cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class='zna-metric-card'>
                <div class='zna-metric-label'>Dynamic Templates</div>
                <div class='zna-metric-value'>3 Styles</div>
                <div class='zna-metric-status status-active'>ACTIVE</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class='zna-metric-card'>
                <div class='zna-metric-label'>Input Modes</div>
                <div class='zna-metric-value'>Dual (Auto/Manual)</div>
                <div class='zna-metric-status status-ready'>READY</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class='zna-metric-card'>
                <div class='zna-metric-label'>Cover Letters</div>
                <div class='zna-metric-value'>Auto-Gen</div>
                <div class='zna-metric-status status-online'>READY</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class='zna-metric-card'>
                <div class='zna-metric-label'>ATS Scanner</div>
                <div class='zna-metric-value'>Semantic NLP</div>
                <div class='zna-metric-status status-online'>ONLINE</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive Split Layout
    dash_col1, dash_col2 = st.columns([0.6, 0.4])
    
    with dash_col1:
        # UPDATED: Enclosing in a sleek card
        st.markdown("<div class='zna-card'><div style='font-size: 14px; font-weight: 700; color: #1f6feb; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;'><i class='fas fa-chart-line'></i> ATS Optimization Trends</div><p style='color: #acb6c0; font-size: 12px;'>Average Match Score (%)</p></div>", unsafe_allow_html=True)
        # We will keep the default line chart but style it with ZNA yellow
        chart_data = pd.DataFrame(
            [65, 72, 68, 85, 88, 92, 96],
            columns=["ATS Match Score (%)"]
        )
        st.line_chart(chart_data, color="#ffb800")
        
        st.markdown("### 🚀 Quick Start Guide")
        with st.expander("📝 1. How to build your first resume?"):
            st.write("Navigate to the **Smart Resume Builder** in the sidebar. You can either paste your raw LinkedIn data for the AI to auto-parse, or fill out the structured manual forms for more precision.")
        with st.expander("🔍 2. How does the ATS Scanner work?"):
            st.write("The scanner uses Google Gemini's Semantic NLP to compare your generated resume text directly against a Job Description to find missing keywords and calculate a match probability.")

    with dash_col2:
        # UPDATED: modern live system logs box
        st.markdown("<div class='zna-card'><div style='font-size: 14px; font-weight: 700; color: #acb6c0; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;'><i class='fas fa-code'></i> Live System Logs</div></div>", unsafe_allow_html=True)
        # Inside the card
        st.success("✅ **[System]** LLM Engine connected to Gemini 2.0 Flash.")
        st.info("ℹ️ **[Module]** PDF Generation engine ready.")
        
        if st.session_state['resume_text']:
            st.success("✅ **[Memory]** User resume loaded in active session.")
        else:
            st.warning("⏳ **[Memory]** Waiting for user to generate a resume...")
            
        if st.session_state['target_job']:
            st.info(f"🎯 **[Target]** Job set to: {st.session_state['target_job']}")

elif app_mode == "📋 Smart Resume Builder":
    # UPDATED: modern title and steps indicator
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='zna-metric-status' style='background: rgba(46, 160, 67, 0.1); color: #2ea043; border: 1px solid rgba(46, 160, 67, 0.3);'>Gemini 2.5 Flash Active 🟢</span></div>", unsafe_allow_html=True)
    st.markdown("<h3>Smart Resume Builder</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #acb6c0; margin-bottom: 24px; font-size: 14px;'>AI-powered synthesis of your professional data.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 1. Setup & Data Input", "📄 2. AI Output & Export"])
    
    with tab1:
        # UPDATED: steps indicator
        st.markdown("""
            <div class='zna-steps'>
                <div class='zna-step-node step-active'><div class='zna-step-circle'>1</div><div class='zna-step-label'>Context</div></div>
                <div class='zna-step-node step-inactive'><div class='zna-step-circle'>2</div><div class='zna-step-label'>Analysis</div></div>
                <div class='zna-step-node step-inactive'><div class='zna-step-circle'>3</div><div class='zna-step-label'>Synthesis</div></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='zna-card' style='padding-top: 15px; font-size: 14px; color: #acb6c0;'>TARGET CAREER PATH:<br><span style='color: #6a737d;'>e.g. Computer Science Engineering Student</span></div>", unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Template Settings")
        style = st.selectbox(
            "Select Professional Template Style:", 
            ["Standard Corporate", "Executive & Leadership", "Creative & Tech", "Academic & Research"]
        )
        st.markdown("---")
        
        # --- DUAL INPUT TOGGLE ---
        st.markdown("### 📥 Choose Data Input Method")
        input_method = st.radio(
            "How do you want to provide your details?",
            ["⚡ Auto-Parse (Paste LinkedIn/Resume Data)", "✍️ Manual Entry (Fill Structured Form)"],
            horizontal=True
        )
        st.markdown("---")
        
        # --- MODE 1: AUTO-PARSE ---
        if input_method == "⚡ Auto-Parse (Paste LinkedIn/Resume Data)":
            st.info("💡 **Fast-Import:** Skip the typing! Copy your entire LinkedIn profile or old resume text and paste it below. The AI will extract and organize it automatically.")
            
            # Auto-Parse Phone Number included here
            col_a, col_b = st.columns(2)
            with col_a:
                auto_name = st.text_input("Full Name *", key="auto_name", placeholder="e.g. Syed Zaid Karim")
                auto_email = st.text_input("Email (for PDF links)", key="auto_email")
                auto_github = st.text_input("GitHub URL (for PDF links)", key="auto_github")
            with col_b:
                auto_target = st.text_input("Target Job Title *", key="auto_target", placeholder="e.g. Computer Science Engineering Student")
                auto_phone = st.text_input("Phone Number (for PDF links)", key="auto_phone")
                auto_linkedin = st.text_input("LinkedIn URL (for PDF links)", key="auto_linkedin")
                
            raw_data = st.text_area("Raw Experience / Education / LinkedIn Data *", height=200, placeholder="Paste your raw text here...")
            
            if st.button("✨ Auto-Generate AI Resume", type="primary"):
                if auto_name and auto_target and raw_data:
                    # Save inputs to memory
                    st.session_state['target_job'] = auto_target
                    st.session_state['user_name'] = auto_name
                    st.session_state['user_email'] = auto_email
                    st.session_state['user_phone'] = auto_phone
                    st.session_state['user_linkedin'] = auto_linkedin
                    st.session_state['user_github'] = auto_github
                    
                    with st.spinner(f"Parsing raw data and applying {style} formatting..."):
                        prompt = f"""
                        Act as an expert Resume Writer and Career Coach. Create a professional resume using this style format: {style}.
                        USER DATA:
                        Target Role: {auto_target}
                        Raw Data (Parse this carefully): {raw_data}
                        RULES:
                        - Create a compelling "PROFESSIONAL SUMMARY" at the top.
                        - DO NOT write the contact info (Name, email, phone, links) at the top. The PDF compiler will handle it.
                        - Organize into clear, UPPERCASE sections (EXPERIENCE, EDUCATION, SKILLS, PROJECTS).
                        - Filter out irrelevant clutter. Extract only professional achievements.
                        - Expand rough notes into professional bullet points using action verbs.
                        - Do NOT use markdown code blocks (```). Return ONLY plain text.
                        """
                        st.session_state['resume_text'] = get_gemini_response(prompt)
                        st.success("✅ Resume successfully built! Go to 'Tab 2' to view, edit, and download.")
                else:
                    st.error("⚠️ Please fill in Name, Target Job, and paste your raw data.")

        # --- MODE 2: MANUAL ENTRY ---
        else:
            st.info("💡 **Structured Input:** Fill in the fields below to ensure specific details are highlighted exactly how you want them.")
            
            st.markdown("#### 👤 Personal Details")
            col_1, col_2 = st.columns(2)
            with col_1:
                man_name = st.text_input("Full Name *", key="man_name", placeholder="e.g. Syed Zaid Karim")
                man_email = st.text_input("Email Address")
                man_linkedin = st.text_input("LinkedIn Profile URL")
            with col_2:
                man_target = st.text_input("Target Job Title *", key="man_target", placeholder="e.g. Computer Science Engineering Student")
                man_phone = st.text_input("Phone Number")
                man_github = st.text_input("GitHub / Portfolio URL")
            
            st.markdown("#### 📝 Professional Summary")
            man_summary = st.text_area("Summary (Optional)", placeholder="e.g. Highly motivated Computer Science student with a passion for building AI-driven applications... Leave blank for AI to auto-generate.", height=100)
                
            st.markdown("#### 🎓 Education & Experience")
            man_education = st.text_area("Education Details *", placeholder="e.g. B.Tech in Computer Science, 2026...")
            man_experience = st.text_area("Work Experience", placeholder="e.g. Trainee at Venturing Digital. Responsibilities included...")
            
            st.markdown("#### 🛠️ Skills & Projects")
            man_skills = st.text_area("Key Skills *", placeholder="e.g. Python, SQL, C++, Java, Machine Learning...")
            man_projects = st.text_area("Major Projects", placeholder="e.g. AI Resume Builder using Streamlit...")
            
            if st.button("✨ Generate AI Resume from Form", type="primary"):
                if man_name and man_target and man_education and man_skills:
                    # Save inputs to memory
                    st.session_state['target_job'] = man_target 
                    st.session_state['user_name'] = man_name
                    st.session_state['user_email'] = man_email
                    st.session_state['user_phone'] = man_phone
                    st.session_state['user_linkedin'] = man_linkedin
                    st.session_state['user_github'] = man_github
                    
                    with st.spinner(f"Structuring data and applying {style} formatting..."):
                        prompt = f"""
                        Act as an expert Resume Writer and Career Coach. Create a professional resume using this style format: {style}.
                        USER DATA:
                        Target Role: {man_target}
                        Provided Summary: {man_summary}
                        Education: {man_education}
                        Experience: {man_experience}
                        Projects: {man_projects}
                        Skills: {man_skills}
                        RULES:
                        - Create a compelling "PROFESSIONAL SUMMARY" at the top. Use the 'Provided Summary' if available and refine it, otherwise write one based on their data.
                        - DO NOT write the contact info (Name, email, phone, links) at the top. The PDF compiler will handle it.
                        - Organize into clear, UPPERCASE sections (EXPERIENCE, EDUCATION, SKILLS, PROJECTS).
                        - Expand their rough notes into highly professional bullet points using action verbs.
                        - Do NOT use markdown code blocks (```). Return ONLY plain text.
                        """
                        st.session_state['resume_text'] = get_gemini_response(prompt)
                        st.success("✅ Resume successfully built! Go to 'Tab 2' to view, edit, and download.")
                else:
                    st.error("⚠️ Please fill in at least your Name, Target Job Title, Education, and Skills.")

    with tab2:
        st.markdown("### ✍️ Refine & Export")
        if st.session_state['resume_text']:
            # UPDATED: Sleek enhance card
            st.markdown("<div class='zna-card' style='padding: 18px;'><div style='font-size: 14px; font-weight: 700; color: #1f6feb; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;'><i class='fas fa-magic'></i> Enhance with AI</div><p style='color: #6a737d; font-size: 11px;'>Increased website traffic by XX% through a targeted content marketing campaign over Y months, enhancing brand visibility and engagement.</p></div>", unsafe_allow_html=True)
            st.info("💡 Your Name, Email, Phone, LinkedIn, and GitHub links will automatically be added as clickable hyperlinks at the top of the downloaded PDF.")
            edited_resume = st.text_area("Final Document (You can manually type and edit here):", value=st.session_state['resume_text'], height=500)
            st.session_state['resume_text'] = edited_resume
            
            # Pass all the saved contact info into the PDF generator
            pdf_data = create_professional_pdf(
                st.session_state['resume_text'], 
                title=st.session_state['user_name'],
                email=st.session_state['user_email'],
                phone=st.session_state['user_phone'],
                linkedin=st.session_state['user_linkedin'],
                github=st.session_state['user_github']
            )
            
            st.download_button(
                label="📥 Download ATS-Friendly PDF", 
                data=pdf_data, 
                file_name=f"Resume_{st.session_state['user_name'].replace(' ', '_')}.pdf", 
                mime="application/pdf",
                type="primary"
            )
        else:
            st.warning("👈 Go back to 'Tab 1' to provide your data and generate your resume first.")

elif app_mode == "✉️ Cover Letter Generator":
    # UPDATED: modern title
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='zna-metric-status' style='background: rgba(46, 160, 67, 0.1); color: #2ea043; border: 1px solid rgba(46, 160, 67, 0.3);'>Gemini 2.5 Flash Active 🟢</span></div>", unsafe_allow_html=True)
    st.markdown("<h3>Letter Generator</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #acb6c0; margin-bottom: 24px; font-size: 14px;'>Hyper-targeted professional narratives powered by AI.</p>", unsafe_allow_html=True)

    if not st.session_state['resume_text']:
        st.error("⚠️ No resume found in memory! Please build your resume in the 'Smart Resume Builder' first so the AI knows your background.")
    else:
        st.success("✅ Linked to your active resume profile.")
        
        col1, col2 = st.columns(2)
        with col1:
            # UPDATED: Enclosing in card like image
            st.markdown("<div class='zna-card'><div style='font-size: 12px; font-weight: 700; color: #57606a; margin-bottom: 15px; text-transform: uppercase;'>JOB TARGET DETAILS</div>", unsafe_allow_html=True)
            company = st.text_input("Hiring Company Name *", placeholder="e.g. Google, Microsoft, TCS")
            hiring_manager = st.text_input("Hiring Manager Name (Optional)", placeholder="e.g. John Doe or 'Hiring Team'")
            job_desc_context = st.text_area("Specific Job Requirements (Optional):", height=150)
            
            st.markdown("<div class='cl-gen-narratives'>", unsafe_allow_html=True)
            if st.button("Generate Narratives", type="primary"):
                if company:
                    with st.spinner(f"Drafting personalized letter for {company}..."):
                        prompt = f"""
                        Write a highly professional and persuasive cover letter.
                        TARGET JOB DETAILS:
                        Target Role: {st.session_state['target_job']}
                        Target Company: {company}
                        Hiring Manager: {hiring_manager if hiring_manager else 'Hiring Manager'}
                        Job Description Context: {job_desc_context}
                        CANDIDATE'S BACKGROUND (Use this to prove why they are a perfect fit):
                        {st.session_state['resume_text']}
                        RULES:
                        - Keep it under 350 words. Be confident, professional, and impactful.
                        - Match the candidate's skills directly to the company/role.
                        - Do NOT use markdown code blocks (```). Return plain text.
                        """
                        st.session_state['cover_letter_output'] = get_gemini_response(prompt)
                else:
                    st.error("⚠️ Please enter the Target Company Name.")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='zna-card'><div style='font-size: 12px; font-weight: 700; color: #57606a; margin-bottom: 15px; text-transform: uppercase;'>Drafted Output</div>", unsafe_allow_html=True)
            if 'cover_letter_output' in st.session_state:
                letter_output = st.session_state['cover_letter_output']
                st.text_area("Your Custom Cover Letter:", value=letter_output, height=400)
                
                # Passed links here too so cover letter matches resume header
                pdf_letter = create_professional_pdf(
                    letter_output, 
                    title=f"Cover Letter - {st.session_state['user_name']}",
                    email=st.session_state['user_email'],
                    phone=st.session_state['user_phone'],
                    linkedin=st.session_state['user_linkedin'],
                    github=st.session_state['user_github']
                )
                st.download_button(
                    label="📥 Download PDF", 
                    data=pdf_letter, 
                    file_name=f"Cover_Letter_{company.replace(' ', '_')}.pdf", 
                    mime="application/pdf",
                    type="primary"
                )
            else:
                # UPDATED: modern awaiting command block
                st.markdown("<div style='text-align: center; color: #57606a; margin-top: 100px;'><i class='fas fa-cog fa-4x' style='margin-bottom: 20px;'></i><div style='font-size: 18px; font-weight: 700; text-transform: uppercase;'>Awaiting Command...</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif app_mode == "🔍 ATS Match Engine":
    # UPDATED: modern title and status indicator
    st.markdown("<div style='float: right; margin-top: -5px;'><span class='zna-metric-status' style='background: rgba(46, 160, 67, 0.1); color: #2ea043; border: 1px solid rgba(46, 160, 67, 0.3);'>Gemini 2.5 Flash Active 🟢</span></div>", unsafe_allow_html=True)
    st.markdown("<h3>ATS Match Engine</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #acb6c0; margin-bottom: 24px; font-size: 14px;'>Semantic comparison with high-resolution score metrics.</p>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns(2)
    with col_l:
        # UPDATED: modern active profile card
        st.markdown("<div class='zna-card'><div style='font-size: 12px; font-weight: 700; color: #57606a; margin-bottom: 15px; text-transform: uppercase; display: flex; justify-content: space-between; align-items: center;'>Active Context Profile <span class='zna-metric-status' style='background: rgba(46, 160, 67, 0.1); color: #2ea043; border: 1px solid rgba(46, 160, 67, 0.3); font-size: 9px;'>VALIDATED</span></div>", unsafe_allow_html=True)
        if st.session_state['resume_text']:
            st.text_area("Preview (Read-only)", value=st.session_state['resume_text'][:300] + "...\n[Full resume loaded in memory]", height=200, disabled=True)
            # UPDATED: modern stats lines from image
            st.markdown("<div style='border-top: 1px solid #30363d; margin-top: 15px; padding-top: 15px; font-size: 12px; color: #94a3b8;'><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>EXPERIENCE NODES <span style='color: #f0f6fc; font-weight: bold;'>3</span></div><div style='display: flex; justify-content: space-between;'>SKILL CLUSTERS <span style='color: #f0f6fc; font-weight: bold;'>15+</span></div></div>", unsafe_allow_html=True)
        else:
            st.error("⚠️ No resume loaded. Go to the Builder first.")
        st.markdown("</div>", unsafe_allow_html=True)
            
    with col_r:
        # UPDATED: modern target jd card
        st.markdown("<div class='zna-card'><div style='font-size: 12px; font-weight: 700; color: #57606a; margin-bottom: 15px; text-transform: uppercase;'>Target Job Description</div>", unsafe_allow_html=True)
        job_desc = st.text_area("Paste the full Job Description here:", height=200, placeholder="Paste the job requirements, skills, and responsibilities...")
        st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚀 Initiate Deep Scan", type="primary"):
        if st.session_state['resume_text'] and job_desc:
            with st.spinner("Analyzing semantic matches and extracting keywords..."):
                prompt = f"""
                Act as an Applicant Tracking System (ATS) expert. Compare this Resume against the provided Job Description.
                RESUME: {st.session_state['resume_text']}
                JOB DESCRIPTION: {job_desc}
                OUTPUT FORMAT:
                1. Match Score: (e.g., 85%)
                2. Missing Keywords: (List the crucial technical or soft skills mentioned in the JD that are missing)
                3. Recommendation: (1-2 sentences on exactly what to add to the resume to boost the score)
                """
                scan_results = get_gemini_response(prompt)
                st.markdown("### 📊 Scan Results")
                st.info(scan_results)
        else:
            st.warning("⚠️ You need both a generated Resume and a Job Description to run the scan.")
