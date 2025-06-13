import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI  # ✅ Correct import
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PyPDF2 import PdfReader
import docx
from gtts import gTTS
import base64
import os

# ✅ Set Google API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCWEgu4uLkd6UNb-1C1G1BZksPc8vOpQb8"

# ✅ Initialize Gemini LLM using LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

# ✅ Streamlit UI Setup
st.set_page_config(page_title="SNS RAG Chatbot", layout="wide")
st.title("📄 SNS RAG Chatbot - Gemini Powered")
st.success("Upload your document and start chatting!")

# ✅ Session States for Memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ File Upload
uploaded_file = st.file_uploader("Upload PDF or DOCX file", type=["pdf", "docx"])

# ✅ Extract Text from Uploaded File
def extract_text(file):
    text = ""
    if file.name.endswith('.pdf'):
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

# ✅ Voice Response Generator
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
    return f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay></audio>'

# ✅ If File is Uploaded
if uploaded_file:
    document_text = extract_text(uploaded_file)

    # ✅ Chat Input
    user_input = st.chat_input("Ask a question from the uploaded document...")

    if user_input:
        # ✅ LangChain Prompt with Chaining
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a helpful assistant. Answer the questions based ONLY on this document: {document_text}"),
            ("user", "{question}")
        ])

        chain = prompt | llm

        response = chain.invoke({"question": user_input})

        # ✅ Store Chat
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response.content))

    # ✅ Display Chat History
    for role, message in st.session_state.chat_history:
        with st.chat_message(role.lower()):
            st.markdown(message)
            if role == "Bot":
                st.markdown(text_to_speech(message), unsafe_allow_html=True)

else:
    st.info("Please upload a PDF or DOCX file to start chatting.")

