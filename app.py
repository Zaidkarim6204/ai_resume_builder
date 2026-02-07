import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. FUNCTIONS ---

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def sanitize_text(text):
    # Fixes special characters that might crash the PDF
    return text.encode('latin-1', 'ignore').decode('latin-1')

def create_professional_pdf(text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Resume / CV", ln=True, align='C')
    pdf.line(10, 25, 200, 25)
    pdf.ln(15)
    pdf.set_font("Arial", size=11)
    
    for line in text_content.split('\n'):
        clean_line = sanitize_text(line)
        # Bold headers logic
        if len(clean_line) < 50 and clean_line.isupper() and len(clean_line.strip()) > 0:
            pdf.set_font("Arial", 'B', 12)
            pdf.ln(5)
            pdf.cell(0, 8, txt=clean_line, ln=True)
            pdf.set_font("Arial", size=11)
        else:
            pdf.multi_cell(0, 6, txt=clean_line)
    return pdf.output(dest='S').encode('latin-1')

def generate_html_resume(text_content):
    html_template = f"""
    <div style="
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        color: #333;
        line-height: 1.6;
    ">
        <h1 style="color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-bottom: 20px;">RESUME PREVIEW</h1>
        <div style="white-space: pre-wrap; font-size: 15px;">
            {text_content}
        </div>
    </div>
    """
    return html_template

# --- 3. UI SETUP ---
st.set_page_config(page_title="AI Resume Architect", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    /* Dark Mode Theme */
    .stApp { background: linear-gradient(to right, #0f0c29, #302b63, #24243e); color: white; }
    section[data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 1px solid #4e4e50; }
    .stTextArea textarea { background-color: #2e2e42; color: white; border-radius: 10px; border: 1px solid #555; }
    
    /* Glowing Buttons */
    div.stButton > button { 
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); 
        color: black; 
        font-weight: bold; 
        border-radius: 20px; 
        border: none;
        transition: transform 0.2s;
    }
    div.stButton > button:hover { transform: scale(1.05); }
    
    /* Headers */
    h1, h2, h3 { color: #f0f0f0; }
</style>
""", unsafe_allow_html=True)

# Header
col_logo, col_title = st.columns([0.1, 0.9])
with col_logo:
    st.markdown("# 🚀")
with col_title:
    st.title("AI Resume Architect")
    st.caption("✨ Professional Career Documentation System | Powered by Google Gemini 2.0")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎛️ Control Panel")
    app_mode = st.radio("Select Mode:", ["Builder Mode (Write)", "ATS Scanner (Check)", "About System"])
    st.markdown("---")
    if app_mode == "Builder Mode (Write)":
        st.info("💡 **Tip:** Be specific! E.g. 'Add a Python skills section with Pandas and SQL'.")
    elif app_mode == "ATS Scanner (Check)":
        st.info("💡 **Tip:** Paste the Job Description to find missing keywords.")

# Session State
if 'resume_text' not in st.session_state:
    st.session_state['resume_text'] = ""

# --- 4. MAIN LAYOUT ---

if app_mode == "Builder Mode (Write)":
    tab1, tab2 = st.tabs(["📝 Editor", "👁️ Live Preview"])
    
    with tab1:
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            st.subheader("Draft Your Content")
            resume_input = st.text_area("Resume Editor", value=st.session_state['resume_text'], height=500, label_visibility="collapsed")
            st.session_state['resume_text'] = resume_input
            
            if st.session_state['resume_text']:
                pdf_data = create_professional_pdf(st.session_state['resume_text'])
                st.download_button(label="💾 Download PDF", data=pdf_data, file_name="Resume.pdf", mime="application/pdf")

        with col2:
            st.subheader("🤖 AI Assistant")
            user_instruction = st.text_area("Instruction:", height=150, placeholder="e.g. 'Rewrite the summary to focus on my Data Analysis internship...'")
            if st.button("✨ Generate"):
                if user_instruction:
                    with st.spinner("AI is thinking..."):
                        # Updated Prompt to fix "Black Box" issue
                        prompt = f"""
                        Act as a professional Resume Writer.
                        CURRENT CONTENT: {st.session_state['resume_text']}
                        INSTRUCTION: {user_instruction}
                        TASK: Update the resume. 
                        - Maintain professional tone.
                        - Use UPPERCASE for section headers.
                        - Use bullet points (*) for lists.
                        - IMPORTANT: Do NOT use markdown code blocks (```). Return ONLY plain text.
                        """
                        response = get_gemini_response(prompt)
                        st.session_state['resume_text'] = response
                        st.rerun()

    with tab2:
        st.subheader("📄 Professional Preview")
        if st.session_state['resume_text']:
            st.markdown(generate_html_resume(st.session_state['resume_text']), unsafe_allow_html=True)
        else:
            st.info("Start writing in the Editor tab to see the preview!")

elif app_mode == "ATS Scanner (Check)":
    st.subheader("🔍 ATS Gap Analysis")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 1. Your Resume")
        if st.session_state['resume_text']:
            st.success("Resume Loaded from Builder Mode")
            st.text_area("Preview", value=st.session_state['resume_text'], height=200, disabled=True)
        else:
            st.warning("⚠️ No Resume found! Go to Builder Mode first.")
            
    with col_r:
        st.markdown("#### 2. Job Description")
        job_desc = st.text_area("Paste JD here:", height=200)
    
    if st.button("📊 Run ATS Scan", type="primary"):
        if st.session_state['resume_text'] and job_desc:
            with st.spinner("Analyzing Match..."):
                prompt = f"Act as ATS. Resume: {st.session_state['resume_text']} JD: {job_desc} Output: Match Score %, Missing Keywords, Advice."
                res = get_gemini_response(prompt)
                st.markdown(res)
        else:
            st.warning("Please ensure you have text in the Builder tab and a JD pasted here.")

elif app_mode == "About System":
    st.subheader("👨‍💻 About this Project")
    st.markdown("""
    ### 🧠 Built with Architecture:
    * **Frontend:** Streamlit (Python-based Reactive UI)
    * **Backend:** Google Gemini 2.0 Flash (LLM)
    * **Document Processing:** FPDF (Python PDF Library)
    
    ### 🎯 Problem Statement
    Traditional ATS (Applicant Tracking Systems) reject **75%** of qualified candidates due to keyword mismatches. 
    
    ### 💡 The Solution
    **AI Resume Architect** uses Generative AI to:
    1.  **Draft** professional content instantly.
    2.  **Analyze** gaps against Job Descriptions.
    3.  **Optimize** resumes for higher hiring probability.
    
    *Developed by Syed Zaid Karim | Final Year Project 2026*
    """)