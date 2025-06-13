import os
import streamlit as st
import requests
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Set your DeepSeek API key
DEEPSEEK_API_KEY = "sk-c9c75cd2936a45a6a34bfe1294a1090c"  # Replace with your actual API key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Function to call DeepSeek API
def call_deepseek_api(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # Use 'deepseek-coder' if you want the coding model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit App UI
st.title("CLT's Digital Tool Finder - SNS Institutions")
st.subheader("Find Free Digital Tools for Teaching, Learning, and Assessment")

# Category Selection
process = st.selectbox("Select a Process", ["Teaching Process", "Learning Process", "Assessment Process"])

# User Input
user_query = st.text_input("Describe your need or challenge:")

if st.button("Find Digital Tools"):
    if user_query:
        with st.spinner("Searching for the best free digital tools..."):
            # Build the query
            prompt = f"""
            Search and recommend 3 to 5 free digital tools available on the web specifically for the {process.lower()}.
            The user is looking for: {user_query}.
            Please list the tool name, website link, and a one-line description for each tool.
            """

            # Call DeepSeek API
            response = call_deepseek_api(prompt)

            st.success("Here are the recommended tools:")
            st.write(response)
    else:
        st.warning("Please enter your requirement to proceed.")
