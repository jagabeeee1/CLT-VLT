import streamlit as st
import requests

# Webhook URL
WEBHOOK_URL = "https://jagabeeee.app.n8n.cloud/webhook-test/4c36ec8a-1ca1-4492-adb0-a26a3c5ed487"

# Streamlit Page Configuration
st.set_page_config(page_title="SNS Intern Task Submission", page_icon="✅", layout="centered")

# Page Heading
st.title("SNS Intern Task Submission")
st.caption("Developed by Jagadeesh.B, SNS Institutions")

# Form Design
with st.form("intern_task_form"):
    st.subheader("Intern Task Submission Form")

    # Input for Intern Name
    intern_name = st.text_input("Intern Name", placeholder="Enter your full name")

    # Dropdown for Team Name
    team_name = st.selectbox(
        "Select Team Name",
        ["CLT", "SCD", "CFC", "IIPC", "SRI", "IQAC"]
    )

    # Input for Weekly Task Summary
    task_summary = st.text_area("Weekly Task Summary", placeholder="Describe your weekly tasks here...", height=150)

    # Submit Button
    submit_button = st.form_submit_button(label="Submit Task")

    # When Submit is Clicked
    if submit_button:
        if intern_name.strip() == "" or task_summary.strip() == "":
            st.warning("Please fill in all the fields before submitting.")
        else:
            # Prepare data payload
            data = {
                "Intern Name": intern_name,
                "Team Name": team_name,
                "Weekly Task Summary": task_summary
            }

            # Send data to n8n webhook
            try:
                response = requests.post(WEBHOOK_URL, json=data)

                if response.status_code == 200:
                    st.success("Task submitted successfully!")
                else:
                    st.error(f"Submission failed. Error code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
