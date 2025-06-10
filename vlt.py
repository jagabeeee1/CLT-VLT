import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Configure Gemini API
genai.configure(api_key="AIzaSyCWEgu4uLkd6UNb-1C1G1BZksPc8vOpQb8")
model = genai.GenerativeModel('gemini-2.0-flash')

# -------------------- Function to Generate Ideas --------------------
def generate_ideas(problem_text, format_style, tone_style):
    prompt = f"Suggest innovative ideas for the following teaching-learning problem:\n\n'{problem_text}'\n\nFormat: {format_style}\nTone: {tone_style}\n\nProvide practical, creative, and actionable ideas."
    response = model.generate_content(prompt)
    return response.text.strip()

# -------------------- Function to Create PDF --------------------
def create_pdf(idea_text, filename="Generated_Ideas.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in idea_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)

# -------------------- Streamlit Frontend --------------------
st.set_page_config(page_title="Idea Generator for Teachers", layout="centered")

st.title("🎯 CLT-Idea Generator for Teaching-Learning Challenges")
st.write("Use this tool to generate creative solutions to your teaching-learning problems using Gemini AI.")

# User Input
problem_input = st.text_area("Enter the teaching-learning problem:", height=150)

# Format & Tone Options
format_option = st.selectbox("Select the desired format:", ["Bullet Points", "Paragraph", "Steps", "Mind Map (Textual)"])
tone_option = st.selectbox("Select the desired tone:", ["Formal", "Informal", "Motivational", "Analytical"])

# Buttons
if st.button("Generate Ideas"):
    if problem_input.strip() == "":
        st.warning("Please enter a teaching-learning problem.")
    else:
        with st.spinner("Generating ideas..."):
            generated_ideas = generate_ideas(problem_input, format_option, tone_option)
            st.success("Ideas generated successfully!")
            st.write("### Generated Ideas:")
            st.write(generated_ideas)

            # Save to PDF
            create_pdf(generated_ideas)
            with open("Generated_Ideas.pdf", "rb") as file:
                st.download_button(label="📥 Download Ideas as PDF", data=file, file_name="Generated_Ideas.pdf", mime="application/pdf")

            # Regenerate Option
            if st.button("Regenerate with New Format/Tone"):
                st.experimental_rerun()

# Instructions
st.sidebar.title("Instructions")
st.sidebar.write("""
1. Enter the teaching-learning problem you face.
2. Select your preferred idea format and tone.
3. Click 'Generate Ideas' to get AI-powered solutions.
4. Download the results as a PDF.
5. Use 'Regenerate' to try different formats or tones.
""")
