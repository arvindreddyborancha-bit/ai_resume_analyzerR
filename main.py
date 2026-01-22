import streamlit as st
import PyPDF2
import docx2txt

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer & Skill Gap Recommendation System")

st.write(
    "Upload your resume (PDF or DOCX) and select the target job role to identify skill gaps."
)

# File uploader
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

role = st.selectbox(
    "Select Target Job Role",
    ["Java Developer", "Data Analyst", "Web Developer"]
)

if st.button("Analyze Resume"):
    if uploaded_file is None:
        st.warning("Please upload a resume file")
    else:
        # 1. Extract text from PDF or DOCX
        resume_text = ""
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = docx2txt.process(uploaded_file)

        if resume_text.strip() == "":
            st.warning("Could not extract text from resume")
        else:
            # 2. Display extracted text (optional)
            st.subheader("Extracted Resume Text")
            st.write(resume_text)

            # 3. Skill Gap Calculation
            role_skills = {
                "Java Developer": ["Java", "OOP", "Spring", "SQL", "Git"],
                "Data Analyst": ["Python", "SQL", "Excel", "Power BI", "Statistics"],
                "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Git"]
            }

            resume_lower = resume_text.lower()
            found_skills = []
            for skill in role_skills[role]:
                if skill.lower() in resume_lower:
                    found_skills.append(skill)

            missing_skills = [skill for skill in role_skills[role] if skill not in found_skills]

            st.subheader("Skill Gap Analysis")
            st.write("Skills Found:", found_skills if found_skills else "None")
            st.write("Missing Skills:", missing_skills if missing_skills else "None")
