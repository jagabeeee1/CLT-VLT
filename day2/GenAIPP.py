import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
import tempfile
import os
import re

# ------------------- CONFIGURE GEMINI -------------------
genai.configure(api_key="AIzaSyCYZge2Zh2fF2Ay_eGB8QCCpz6QB6QGQAQ")
model = genai.GenerativeModel("gemini-2.0-flash")

# ------------------- APP HEADER -------------------
st.markdown("<h1 style='text-align:center; font-weight:bold;'>SNS Gen AI-Placement Prep Tool</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Developed by Jagadeesh B, CLT Coordinator, SNS Institutions</h4>", unsafe_allow_html=True)
st.image("https://www.snsct.org/images/placements.png", use_container_width=True)

# ------------------- USER INPUTS -------------------
st.subheader("📌 Choose Your Practice Options")

section = st.radio("Select Section", ["Verbal", "Quantitative Aptitude", "Reasoning", "Domain", "Programming Language", "Coding", "HR Interview"])

topic = st.text_input("Enter the Topic (e.g., Probability, Python Loops, Resume Tips, etc.)")

q_type = st.radio("Select Question Type", ["MCQ", "Descriptive", "Question Stem", "Debugging", "Coding"])

answer_option = st.radio("With or Without Answers", ["With Answers", "Without Answers"])

num_questions = st.number_input("Enter Number of Questions", min_value=1, max_value=50, value=5)

difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium", "Hard"])

# ------------------- GENERATE QUESTIONS -------------------
if st.button("Generate Questions"):
    with st.spinner("⏳ Generating your practice questions..."):
        prompt = f"""
        Generate {num_questions} {q_type} questions for {section}.
        Topic: {topic}.
        Difficulty: {difficulty}.
        Provide questions {answer_option.lower()}.
        Format them neatly for placement preparation.
        """
        response = model.generate_content(prompt)
        generated_text = response.text if response else "No response from Gemini API."

        # 🔹 Clean the text from **bold**, markdown or unwanted symbols
        clean_text = re.sub(r"[*_#`]+", "", generated_text)

        st.success("✅ Questions Generated Successfully!")
        st.text_area("Generated Questions", clean_text, height=400)

        # ------------------- PDF DOWNLOAD -------------------
        def create_pdf(text):
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))  # Unicode font support
            styles = getSampleStyleSheet()
            custom_style = ParagraphStyle(
                name="CustomStyle",
                fontName="Times-Roman",
                fontSize=12,
                leading=15,
                alignment=0
            )

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            doc = SimpleDocTemplate(temp_file.name, pagesize=A4)

            elements = []
            header_style = ParagraphStyle(
                name="Header",
                fontName="Times-Bold",
                fontSize=14,
                alignment=1
            )
            subheader_style = ParagraphStyle(
                name="SubHeader",
                fontName="Times-Roman",
                fontSize=12,
                alignment=1
            )

            # Add header
            elements.append(Paragraph("SNS Center for Learning & Teaching", header_style))
            elements.append(Paragraph("Coimbatore", subheader_style))
            elements.append(Spacer(1, 0.3 * inch))

            # Add body content
            for line in text.split("\n"):
                if line.strip():
                    elements.append(Paragraph(line.strip(), custom_style))
                    elements.append(Spacer(1, 0.1 * inch))

            doc.build(elements)
            return temp_file.name

        pdf_path = create_pdf(clean_text)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name="SNS_Placement_Questions.pdf",
                mime="application/pdf"
            )
        os.unlink(pdf_path)  # cleanup temp file
