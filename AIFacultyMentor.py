import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCWEgu4uLkd6UNb-1C1G1BZksPc8vOpQb8")  # Replace with your API Key

# Streamlit Page Configuration
st.set_page_config(page_title="AI Faculty Mentor", page_icon="🎓", layout="centered")

# App Title
st.markdown("""
# AI Faculty Mentor
### Developed by Jagadeesh B, CLT Coordinator, SNS Institutions
""")

# App Description
st.write("""
Welcome to **AI Faculty Mentor**, an idea generation platform designed for college teachers to explore solutions for the challenges faced in Academic and Administrative Processes. 
Please select your challenge area, describe your need, and choose the tone for the idea you would like to receive.
""")

# UI Styling
st.markdown("""
<style>
    body {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        background-color: white !important;
    }
    .stSelectbox > div > div > div {
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Dropdown for Challenge Area
challenge_area = st.selectbox(
    "Select the Challenge Area",
    ["Teaching & Learning", "Activities for Teaching", "Assessment", "Subject Content", "Student Handling", "Project", "Internship", "Others"]
)

# Additional input if 'Others' is selected
if challenge_area == "Others":
    other_area = st.text_input("Please specify the area")
else:
    other_area = challenge_area

# Text Input for User Challenge
user_input = st.text_area("Describe your need or challenge in detail")

# Tone Selection
tone = st.radio("Select the tone for idea generation", ["Normal", "Friendly", "Strict"])

# Generate Ideas Button
if st.button("Generate Ideas"):
    if user_input.strip() == "":
        st.warning("Please enter your challenge description.")
    else:
        prompt = f"""Generate some innovative and practical ideas for the following academic or administrative challenge:
        
        Challenge Area: {other_area}
        Description: {user_input}
        Tone: {tone}
        
        Provide clear and actionable suggestions."""

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        generated_ideas = response.text

        st.subheader("Generated Ideas")
        st.write(generated_ideas)

        # Unicode Fix: Remove unsupported characters
        generated_ideas = ''.join(c for c in generated_ideas if ord(c) < 256)

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", '', 12)
        pdf.multi_cell(0, 10, f"AI Faculty Mentor\nDeveloped by Jagadeesh B, CLT Coordinator, SNS Institutions\n\n")
        pdf.multi_cell(0, 10, f"Challenge Area: {other_area}\n")
        pdf.multi_cell(0, 10, f"Challenge Description: {user_input}\n")
        pdf.multi_cell(0, 10, f"Tone: {tone}\n\n")
        pdf.multi_cell(0, 10, "Generated Ideas:\n")
        pdf.multi_cell(0, 10, generated_ideas)

        pdf_output = "AI_Faculty_Mentor_Ideas.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as file:
            st.download_button(
                label="Download Ideas as PDF",
                data=file,
                file_name=pdf_output,
                mime="application/pdf"
            )
