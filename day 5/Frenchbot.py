import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from gtts import gTTS
import base64

# Set API key (or use env var GOOGLE_API_KEY)
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCWEgu4uLkd6UNb-1C1G1BZksPc8vOpQb8'  # Replace with your Gemini API key

st.set_page_config(page_title="English→French Translator with Voice", page_icon="🌐")
st.title("🌐 English to French Translator with Voice Output")

# User input
english_text = st.text_input("Enter English sentence:")

# Translate button
if st.button("Translate and Speak"):
    if not english_text.strip():
        st.warning("Please enter something to translate.")
    else:
        try:
            # LangChain Setup
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

            prompt = ChatPromptTemplate.from_messages([
                ("system", "Translate the user input to French."),
                ("human", "{input}")
            ])

            chain: Runnable = prompt | llm
            result = chain.invoke({"input": english_text})
            translated = result.content

            st.success("✅ Translation successful!")
            st.write(f"**French:** {translated}")

            # Text to Speech using gTTS
            tts = gTTS(text=translated, lang='fr')
            audio_file = "translation.mp3"
            tts.save(audio_file)

            # Play the audio
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")

        except Exception as err:
            st.error(f"Error: {err}")
