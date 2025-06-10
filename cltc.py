import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io

# ========== Gemini API Setup ==========
genai.configure(api_key="AIzaSyCWEgu4uLkd6UNb-1C1G1BZksPc8vOpQb8")  # Replace with your API Key
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# ========== Streamlit App Setup ==========
st.set_page_config(page_title="SNS - CLT’s Contest Finder", layout="centered")

st.title("SNS - CLT’s Contest Finder")
st.caption("(Jagadeesh, B, CLT Coordinator, SNS Institutions)")
st.write("🔍 **Find Upcoming Hackathons and Contests to Participate!**")

# ========== User Inputs ==========
user_input = st.text_input("Enter a keyword or topic to find relevant hackathons:")

format_option = st.radio("Select Output Format:", ["Table", "Bullet Points"])
tone_option = st.radio("Select Tone:", ["Average", "Good", "Best"])

# ========== Gemini API Fetching Function ==========
def fetch_hackathons(user_input, tone_option):
    prompt = f"""
    List the upcoming hackathons in India for college students related to {user_input} in {tone_option} tone. 
    Provide the following details for each hackathon: Event Name - Last Date (dd-mm-yyyy) - Registration URL. 
    Exclude completed events. Show minimum 5 hackathons.
    """
    response = model.generate_content(prompt)
    return response.text

# ========== Parsing Function ==========
def parse_response(response_text):
    lines = response_text.strip().split('\n')
    events = []
    for line in lines:
        parts = line.split(' - ')
        if len(parts) == 3:
            event_name, last_date, url = parts
            try:
                event_date = datetime.strptime(last_date.strip(), "%d-%m-%Y")
                if event_date >= datetime.now():
                    events.append({"Event Name": event_name.strip(), "Last Date": last_date.strip(), "URL": url.strip()})
            except:
                continue
    return pd.DataFrame(events)

# ========== PDF Creation Function ==========
def create_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="SNS - CLT’s Contest Finder", ln=True, align='C')
    pdf.cell(200, 10, txt="(Jagadeesh, B, CLT Coordinator, SNS Institutions)", ln=True, align='C')
    pdf.ln(10)

    for index, row in dataframe.iterrows():
        pdf.cell(0, 10, f"Event: {row['Event Name']}", ln=True)
        pdf.cell(0, 10, f"Last Date: {row['Last Date']}", ln=True)
        pdf.cell(0, 10, f"URL: {row['URL']}", ln=True)
        pdf.ln(5)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# ========== Main Logic ==========
if 'regenerate' not in st.session_state:
    st.session_state['regenerate'] = False

if st.button("Generate Hackathon List") or st.session_state['regenerate']:
    if user_input:
        response = fetch_hackathons(user_input, tone_option)
        df = parse_response(response)

        if not df.empty:
            st.write("### Upcoming Hackathons")
            if format_option == "Table":
                st.dataframe(df)
            else:
                for index, row in df.iterrows():
                    st.write(f"- **{row['Event Name']}** | Last Date: {row['Last Date']} | [Register Here]({row['URL']})")
            st.session_state['df'] = df
        else:
            st.warning("No upcoming hackathons found. Try a different keyword or tone.")
        st.session_state['regenerate'] = False

# ========== PDF Download ==========
if 'df' in st.session_state and not st.session_state['df'].empty:
    pdf_file = create_pdf(st.session_state['df'])
    st.download_button(
        label="📄 Download Hackathon List as PDF",
        data=pdf_file,
        file_name="hackathon_list.pdf",
        mime="application/pdf"
    )

# ========== Regenerate Button ==========
if st.button("Regenerate Hackathon List"):
    st.session_state['regenerate'] = True
    st.experimental_rerun()
