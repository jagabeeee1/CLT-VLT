import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

# Set API key (or use env var GOOGLE_API_KEY)
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCWEgu4uLkd6UNb-1C1G1BZksPc8vOpQb8'

st.set_page_config(page_title="English→French Translator", page_icon="🌐")
st.title("🌐 English to French Translator (Gemini via LangChain)")

english_text = st.text_input("Enter English sentence:")

if st.button("Translate"):
    if not english_text.strip():
        st.warning("Please enter something to translate.")
    else:
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  # from langchain_google_genai

            prompt = ChatPromptTemplate.from_messages([
                ("system", "Translate the user input to French."),
                ("human", "{input}")
            ])

            chain: Runnable = prompt | llm
            result = chain.invoke({"input": english_text})
            translated = result.content

            st.success("✅ Translation successful!")
            st.write(f"**French:** {translated}")

        except Exception as err:
            st.error(f"Error: {err}")
