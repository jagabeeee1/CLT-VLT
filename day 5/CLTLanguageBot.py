import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from gtts import gTTS
import base64

# --- Set your Gemini API Key ---
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCYZge2Zh2fF2Ay_eGB8QCCpz6QB6QGQAQ'  # Replace with your Gemini API key

# --- Streamlit Page Setup ---
st.set_page_config(page_title="CLT's Language Learning - SNS Institutions", page_icon="🌐")
st.title("🌐 CLT's Language Learning - SNS Institutions")

# --- User Input ---
english_text = st.text_input("Enter an English sentence to translate:")

# --- LangChain Setup ---
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# --- Translation Function ---
def translate_and_speak(target_language, lang_code):
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"Translate the user input to {target_language}."),
            ("human", "{input}")
        ])

        chain: Runnable = prompt | llm
        result = chain.invoke({"input": english_text})
        translated = result.content

        st.success(f"✅ Translated to {target_language} successfully!")
        st.write(f"**{target_language} Translation:** {translated}")

        # Text to Speech using gTTS
        tts = gTTS(text=translated, lang=lang_code)
        audio_file = f"{target_language}.mp3"
        tts.save(audio_file)

        # Play the audio
        audio_bytes = open(audio_file, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")

    except Exception as err:
        st.error(f"Error: {err}")

# --- Buttons for Each Language ---
col1, col2, col3, col4 = st.columns(4)

if english_text.strip():
    with col1:
        if st.button("Translate to French"):
            translate_and_speak("French", "fr")

    with col2:
        if st.button("Translate to Japanese"):
            translate_and_speak("Japanese", "ja")

    with col3:
        if st.button("Translate to German"):
            translate_and_speak("German", "de")

    with col4:
        if st.button("Translate to Hindi"):
            translate_and_speak("Hindi", "hi")
else:
    st.info("Please enter a sentence to enable translation.")

