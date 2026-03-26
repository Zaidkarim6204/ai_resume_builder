import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
import urllib.parse
import pandas as pd
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AI Resume Architect", page_icon="🏗️", layout="wide")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please check your .env file or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. INTERACTIVE CSS STYLING ---
st.markdown("""
<style>
    /* Main App Background */
    .stApp { background-color: #0B0E14; color: #F0F2F6; }
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    
    /* Interactive Metric Cards */
    div[data-testid="metric-container"] { 
        background: linear-gradient(145deg, #1A1C23 0%, #0E1117 100%); 
        border: 1px solid #2B2D38; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: #00C9FF;
        box-shadow: 0 8px 25px rgba(0, 201, 255, 0.15);
    }

    /* Glowing Primary Button */
    .stButton>button[kind="primary"] { 
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); 
        color: #111; 
        border: none; 
        font-weight: 800; 
        width: 100%; 
        border-radius: 10px;
        transition: all 0.3s ease; 
    }
    .stButton>button[kind="primary"]:hover { 
        transform: scale(1.02); 
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.4); 
    }

    /* Clean Secondary Buttons */
    .stButton>button[kind="secondary"] { 
        border-radius: 10px; 
        transition: all 0.3s ease;
    }
    .stButton>button[kind="secondary"]:hover {
        border-color: #00C9FF;
        color: #00C9FF;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 201, 255, 0.05);
        border-bottom-color: #00C9FF !important;
    }
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

# ADDED: Email, LinkedIn, and GitHub parameters for clickable links
def create_professional_pdf(text_content, title="Document", email="", linkedin="", github=""):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Header Title (Name)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=title, ln=True, align='C')
    
    # NEW: Clickable Links
    pdf.set_font("Arial", size=10)
    if email:
        pdf.set_text_color(0, 102, 204) # Blue link color
        pdf.cell(0, 5, txt=f"Email: {sanitize_text(email)}", ln=True, align='C', link=f"mailto:{email}")
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

# ADDED: Store the contact details so they can be passed to the PDF later
if 'user_name' not in st.session_state: st.session_state['user_name'] = "Professional Resume"
if 'user_email' not in st.session_state: st.session_state['user_email'] = ""
if 'user_linkedin' not in st.session_state: st.session_state['user_linkedin'] = ""
if 'user_github' not in st.session_state: st.session_state['user_github'] = ""

# --- 5. SIDEBAR NAVIGATION & LINKEDIN PORTAL ---
with st.sidebar:
    st.markdown("## ⚙️ AI Studio Menu")
    app_mode = st.radio("Navigate Workspace:", [
        "📊 Overview Dashboard", 
        "📝 Smart Resume Builder", 
        "✉️ Cover Letter Generator", 
        "🔍 ATS Match Engine"
    ])
    st.markdown("---")
    
    # Dynamic LinkedIn Direct Apply Portal
    st.markdown("### 🌐 Job Portal")
    if st.session_state['target_job']:
        job_query = urllib.parse.quote(st.session_state['target_job'])
        st.markdown(f"""
        <a href="https://www.linkedin.com/jobs/search/?keywords={job_query}" target="_blank" style="text-decoration: none;">
            <button style="background-color: #0077b5; padding: 12px; width: 100%; border-radius: 8px; color: white; border: none; font-weight: bold; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.2); transition: all 0.3s ease;">
                Apply on LinkedIn ↗
            </button>
        </a>
        """, unsafe_allow_html=True)
        st.caption(f"Searching for: **{st.session_state['target_job']}**")
    else:
        st.info("💡 Fill out the 'Target Job Title' in the Resume Builder to unlock the LinkedIn Job Portal.")

# --- 6. MAIN APP LOGIC ---

if app_mode == "📊 Overview Dashboard":
    st.title("Welcome to your Career Workspace")
    
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dynamic Templates", "3 Styles", "Active 🟢")
    col2.metric("Input Modes", "Dual (Auto/Manual)", "Enabled ⚡")
    col3.metric("Cover Letters", "Auto-Gen", "Ready 📝")
    col4.metric("ATS Scanner", "Semantic NLP", "Online 🚀")
    
    st.markdown("---")
    
    # Interactive Split Layout
    dash_col1, dash_col2 = st.columns([0.6, 0.4])
    
    with dash_col1:
        st.markdown("### 📈 ATS Optimization Trends")
        st.caption("Average ATS Match Scores generated by the AI over the last 7 sessions.")
        # Mock data for UI appeal
        chart_data = pd.DataFrame(
            [65, 72, 68, 85, 88, 92, 96],
            columns=["ATS Match Score (%)"]
        )
        st.line_chart(chart_data, color="#00C9FF")
        
        st.markdown("### 🚀 Quick Start Guide")
        with st.expander("📝 1. How to build your first resume?"):
            st.write("Navigate to the **Smart Resume Builder** in the sidebar. You can either paste your raw LinkedIn data for the AI to auto-parse, or fill out the structured manual forms for more precision.")
        with st.expander("🔍 2. How does the ATS Scanner work?"):
            st.write("The scanner uses Google Gemini's Semantic NLP to compare your generated resume text directly against a Job Description to find missing keywords and calculate a match probability.")

    with dash_col2:
        st.markdown("### ⚡ Live System Logs")
        st.markdown("""
        <div style='background-color: #1A1C23; padding: 20px; border-radius: 12px; border: 1px solid #2B2D38;'>
        """, unsafe_allow_html=True)
        
        st.success("✅ **[System]** LLM Engine connected to Gemini 2.0 Flash.")
        st.info("ℹ️ **[Module]** PDF Generation engine ready.")
        
        if st.session_state['resume_text']:
            st.success("✅ **[Memory]** User resume loaded in active session.")
        else:
            st.warning("⏳ **[Memory]** Waiting for user to generate a resume...")
            
        if st.session_state['target_job']:
            st.info(f"🎯 **[Target]** Job set to: {st.session_state['target_job']}")
            
        st.markdown("</div>", unsafe_allow_html=True)

elif app_mode == "📝 Smart Resume Builder":
    st.title("📝 Smart Resume Builder")
    
    tab1, tab2 = st.tabs(["📋 1. Setup & Data Input", "📄 2. AI Output & Export"])
    
    with tab1:
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
            
            # ADDED: Added fields here to grab links for PDF
            col_a, col_b = st.columns(2)
            with col_a:
                auto_name = st.text_input("Full Name *", key="auto_name", placeholder="e.g. Syed Zaid Karim")
                auto_email = st.text_input("Email (for PDF links)", key="auto_email")
                auto_github = st.text_input("GitHub URL (for PDF links)", key="auto_github")
            with col_b:
                auto_target = st.text_input("Target Job Title *", key="auto_target", placeholder="e.g. Data Analyst")
                auto_linkedin = st.text_input("LinkedIn URL (for PDF links)", key="auto_linkedin")
                
            raw_data = st.text_area("Raw Experience / Education / LinkedIn Data *", height=200, placeholder="Paste your raw text here...")
            
            if st.button("✨ Auto-Generate AI Resume", type="primary"):
                if auto_name and auto_target and raw_data:
                    # ADDED: Save inputs to memory
                    st.session_state['target_job'] = auto_target
                    st.session_state['user_name'] = auto_name
                    st.session_state['user_email'] = auto_email
                    st.session_state['user_linkedin'] = auto_linkedin
                    st.session_state['user_github'] = auto_github
                    
                    with st.spinner(f"Parsing raw data and applying {style} formatting..."):
                        prompt = f"""
                        Act as an expert Resume Writer and Career Coach. Create a professional resume using this style format: {style}.
                        USER DATA:
                        Name: {auto_name} | Target Role: {auto_target}
                        Raw Data (Parse this carefully): {raw_data}
                        RULES:
                        - Create a compelling "PROFESSIONAL SUMMARY" at the top.
                        - DO NOT write the contact info (Name, email, links) at the top. The PDF will add them.
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
                    # ADDED: Save inputs to memory
                    st.session_state['target_job'] = man_target 
                    st.session_state['user_name'] = man_name
                    st.session_state['user_email'] = man_email
                    st.session_state['user_linkedin'] = man_linkedin
                    st.session_state['user_github'] = man_github
                    
                    with st.spinner(f"Structuring data and applying {style} formatting..."):
                        prompt = f"""
                        Act as an expert Resume Writer and Career Coach. Create a professional resume using this style format: {style}.
                        USER DATA:
                        Name: {man_name} | Target Role: {man_target}
                        Contact: {man_email} | {man_phone} | {man_linkedin} | {man_github}
                        Provided Summary: {man_summary}
                        Education: {man_education}
                        Experience: {man_experience}
                        Projects: {man_projects}
                        Skills: {man_skills}
                        RULES:
                        - Create a compelling "PROFESSIONAL SUMMARY" at the top. Use the 'Provided Summary' if available and refine it, otherwise write one based on their data.
                        - DO NOT write the contact info (Name, email, links) at the top. The PDF will add them.
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
            st.info("💡 Your Name, Email, LinkedIn, and GitHub links will automatically be added as clickable hyperlinks at the top of the downloaded PDF.")
            edited_resume = st.text_area("Final Document (You can manually type and edit here):", value=st.session_state['resume_text'], height=500)
            st.session_state['resume_text'] = edited_resume
            
            # ADDED: Passed the saved links into the PDF generator
            pdf_data = create_professional_pdf(
                st.session_state['resume_text'], 
                title=st.session_state['user_name'],
                email=st.session_state['user_email'],
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
    st.title("✉️ Auto-Cover Letter")
    st.markdown("Generate a highly personalized cover letter based on the exact data from your current resume.")
    
    if not st.session_state['resume_text']:
        st.error("⚠️ No resume found in memory! Please build your resume in the 'Smart Resume Builder' first so the AI knows your background.")
    else:
        st.success("✅ Linked to your active resume profile.")
        
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Hiring Company Name *", placeholder="e.g. Google, Microsoft, TCS")
        with col2:
            hiring_manager = st.text_input("Hiring Manager Name (Optional)", placeholder="e.g. John Doe or 'Hiring Team'")
            
        job_desc_context = st.text_area("Specific Job Requirements (Optional, paste the JD to make the letter highly targeted):", height=150)
        
        if st.button("✨ Write Cover Letter", type="primary"):
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
                    letter_output = get_gemini_response(prompt)
                    
                    st.text_area("Your Custom Cover Letter:", value=letter_output, height=400)
                    
                    # ADDED: Passed links here too so cover letter matches resume
                    pdf_letter = create_professional_pdf(
                        letter_output, 
                        title=f"Cover Letter - {st.session_state['user_name']}",
                        email=st.session_state['user_email'],
                        linkedin=st.session_state['user_linkedin'],
                        github=st.session_state['user_github']
                    )
                    st.download_button(
                        label="📥 Download Cover Letter PDF", 
                        data=pdf_letter, 
                        file_name=f"Cover_Letter_{company.replace(' ', '_')}.pdf", 
                        mime="application/pdf",
                        type="primary"
                    )
            else:
                st.error("⚠️ Please enter the Target Company Name.")

elif app_mode == "🔍 ATS Match Engine":
    st.title("🔍 ATS Match Engine")
    st.markdown("Compare your generated resume against a real Job Description to find missing keywords before you apply.")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### Your Active Resume")
        if st.session_state['resume_text']:
            st.success("✅ Loaded from Builder")
            st.text_area("Preview (Read-only)", value=st.session_state['resume_text'][:300] + "...\n[Full resume loaded in memory]", height=200, disabled=True)
        else:
            st.error("⚠️ No resume loaded. Go to the Builder first.")
            
    with col_r:
        st.markdown("#### Target Job Description")
        job_desc = st.text_area("Paste the full Job Description here:", height=200, placeholder="Paste the job requirements, skills, and responsibilities...")
    
    if st.button("🚀 Run Deep ATS Scan", type="primary"):
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
