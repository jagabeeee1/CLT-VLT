import os
import streamlit as st
from langchain.chat_models import ChatOpenAI  # Using ChatOpenAI for Deepseek API structure
from langchain.schema import HumanMessage
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType

# Set your Deepseek API Key
os.environ["OPENAI_API_KEY"] = "sk-c9c75cd2936a45a6a34bfe1294a1090c"  # Replace with your Deepseek API key

# Initialize the Deepseek LLM using OpenAI API format
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# Initialize DuckDuckGo Search Tool
search_tool = DuckDuckGoSearchRun()

# Initialize LangChain Agent with Deepseek and DuckDuckGo Search
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Streamlit App UI
st.title("Gold Rate Today - Live Finder (Deepseek LLM)")
st.subheader("Get the latest gold rates in your city")

# Gold Type Selection
gold_type = st.selectbox("Select Gold Type", ["22K", "24K", "18K"])

# Location Input
location = st.text_input("Enter your City or Country:")

if st.button("Find Gold Rate"):
    if location:
        with st.spinner("Fetching latest gold rates..."):
            # Build the query for the agent
            prompt = f"""
            Find the current gold rate for {gold_type} gold in {location}.
            Please provide the price per gram or per 10 grams in the local currency.
            Also mention the source of the information if available.
            """

            # Run the agent to fetch the gold rate using DuckDuckGo and Deepseek
            response = agent.run(prompt)

            st.success("Here is the latest gold rate:")
            st.write(response)
    else:
        st.warning("Please enter your city or country to proceed.")
