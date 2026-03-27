# 🏗️ ZNA - AI Resume Architect

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-Flash_2.0-8E75B2)
![Status](https://img.shields.io/badge/Status-Active-success)

**ZNA AI Resume Architect** is a next-generation, LLM-powered career document synthesizer designed to help professionals and students build ATS-optimized resumes, generate highly targeted cover letters, and analyze job descriptions using Semantic NLP. 

Developed as a Final Year Computer Science Engineering Project.

---

## ✨ Core Features

* **🤖 Dual-Mode Smart Resume Builder:** * **Auto-Parse Engine:** Simply paste raw LinkedIn profile data or rough notes, and the AI will automatically extract, format, and categorize the information.
    * **Structured Manual Entry:** A granular form-based input for users who want precise control over every detail.
* **🎨 Dynamic Style Templates:** Instantly format the output into distinct professional styles: *Standard Corporate, Executive & Leadership, Creative & Tech, or Academic & Research*.
* **📄 Smart PDF Export:** Automatically compiles the AI-generated text into a clean, ATS-friendly PDF. **Contact details (Email, Phone, LinkedIn, GitHub) are automatically injected as clickable blue hyperlinks** in the document header.
* **✉️ Auto-Cover Letter Generator:** Contextually generates highly persuasive, sub-350-word cover letters by mapping the user's active resume data against a specific target company and job description.
* **🔍 Semantic ATS Match Engine:** Uses deep NLP to compare the generated resume against a raw Job Description (JD). It calculates a match score, identifies missing crucial keywords, and provides actionable recommendations.
* **🌐 Live Job Portal Integration:** Dynamically generates a direct LinkedIn job search query based on the user's target role.
* **💎 Premium UI/UX:** Features a custom, glassmorphism-styled dark mode interface with interactive metrics and live system logs.

---

## 🛠️ Tech Stack

* **Frontend & Framework:** Streamlit (Python) + Custom CSS
* **Generative AI / LLM:** Google Gemini API (`gemini-flash-latest`)
* **Document Generation:** `fpdf` (Python PDF generation library)
* **Data Handling:** `pandas`
* **Environment Management:** `python-dotenv`

---

## 🚀 Local Installation & Setup

To run this application locally on your machine, follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR-USERNAME/ai_resume_builder.git](https://github.com/YOUR-USERNAME/ai_resume_builder.git)
cd ai_resume_builder
2. Create a virtual environment

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
3. Install dependencies

Bash
pip install streamlit google-generativeai fpdf pandas python-dotenv
4. Set up your Environment Variables
Create a file named .env in the root directory of the project and add your Google Gemini API key:

Code snippet
GOOGLE_API_KEY="your_actual_api_key_here"
5. Run the Application

Bash
streamlit run app.py
💡 Usage Guide
Dashboard: Start at the Overview Dashboard to view system status and ATS optimization trends.

Build Resume: Navigate to the Smart Resume Builder. Choose a template style, input your data via Auto-Parse or Manual Form, and click Generate.

Export: Switch to the "AI Output & Export" tab to make final edits and download your PDF with clickable links.

Cover Letter: Go to the Cover Letter Generator, input the hiring company, and let the AI draft a targeted letter based on your active resume.

Scan: Use the ATS Match Engine to paste a real Job Description and see how well your new resume scores.
