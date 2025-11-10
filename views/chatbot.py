import streamlit as st
from streamlit_option_menu import option_menu
import os
import time

# Core prompt template
from langchain_core.prompts import PromptTemplate

# Core prompt template
from langchain_core.prompts import PromptTemplate

# Memory (from langchain-classic)
from langchain_classic.memory import ConversationBufferMemory

# Chains (from langchain-classic)
from langchain_classic.chains import RetrievalQA

# Text splitter (from langchain-text-splitters)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Community integrations
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader



# Callbacks
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.callbacks.manager import CallbackManager

# Voice
import pyttsx3
import speech_recognition as sr
from streamlit_pdf_viewer import pdf_viewer

# Setup folders
os.makedirs('pdfFiles', exist_ok=True)
os.makedirs('vectorDB', exist_ok=True)

# Voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def SpeakNow(command):
    voice = pyttsx3.init()
    voice.say(command)
    voice.runAndWait()

audio = sr.Recognizer()

# Session state setup
if 'template' not in st.session_state:
    st.session_state.template = """You are a knowledgeable chatbot, here to help with questions of the user. Your tone should be professional and informative.

Context: {context}
History: {history}

User: {question}
Chatbot:"""

if 'prompt' not in st.session_state:
    st.session_state.prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template=st.session_state.template,
    )

if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        input_key="question",
        chat_memory=StreamlitChatMessageHistory()
    )

if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = Chroma(
        persist_directory='vectorDB',
        embedding_function=OllamaEmbeddings(base_url='http://localhost:11434', model="llama3")
    )

if 'llm' not in st.session_state:
    st.session_state.llm = Ollama(
        base_url="http://localhost:11434",
        model="llama3",
        verbose=True
    )



if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# UI
st.header("LocoChat - Your Friendly Document Assistant 👀")

def multipage_menu(caption):
    st.sidebar.title(caption)
    st.sidebar.subheader('Navigation')
    st.sidebar.image('assets/ss.png')

multipage_menu("LocoChat")

selected = option_menu(
    menu_title="Main Menu",
    options=["Home", "History", "Voice Text"],
    icons=["house", "book", "mic"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Voice input
if selected == "Voice Text":
    with sr.Microphone() as source2:
        with st.spinner('Listening...'):
            time.sleep(5)
        audio.adjust_for_ambient_noise(source2, duration=2)
        st.write("Speak now please...")
        audio2 = audio.listen(source2)
        text = audio.recognize_google(audio2).lower()
        say = "Did you say " + text
        SpeakNow(say)
        st.chat_input(text)

# PDF history viewer
if selected == "History":
    pdf_folder = "pdfFiles"
    pdf_files = [f"{pdf_folder}/{filename}" for filename in os.listdir(pdf_folder) if filename.lower().endswith(".pdf")]
    selected_pdf = st.selectbox("Select a PDF file", pdf_files)
    with open(selected_pdf, "rb") as f:
        binary_data = f.read()
        pdf_viewer(input=binary_data, width=700)

# Home tab
if selected == "Home":
    st.title(f"You have selected {selected}")
    col1, col2 = st.columns(2)
    with col1:
        st.image("./assets/robot-lunch.gif")
    with col2:
        st.title("What can I do for You?")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    if uploaded_file is not None:
        st.text("File uploaded successfully")
        file_path = f'pdfFiles/{uploaded_file.name}'
        if not os.path.exists(file_path):
            with st.status("Saving file..."):
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.read())

                loader = PyPDFLoader(file_path)
                data = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
                all_splits = text_splitter.split_documents(data)

                st.session_state.vectorstore = Chroma.from_documents(
                    documents=all_splits,
                    embedding=OllamaEmbeddings(model="llama3")
                )
                st.session_state.vectorstore.persist()

        st.session_state.retriever = st.session_state.vectorstore.as_retriever()

        if 'qa_chain' not in st.session_state:
            st.session_state.qa_chain = RetrievalQA.from_chain_type(
                llm=st.session_state.llm,
                chain_type='stuff',
                retriever=st.session_state.retriever,
                verbose=True,
                chain_type_kwargs={
                    "verbose": True,
                    "prompt": st.session_state.prompt,
                    "memory": st.session_state.memory,
                }
            )

        if user_input := st.chat_input("You:", key="user_input"):
            user_message = {"role": "user", "message": user_input}
            st.session_state.chat_history.append(user_message)
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking answer..."):
                    response = st.session_state.qa_chain(user_input)
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response['result'].split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

            chatbot_message = {"role": "assistant", "message": response['result']}
            st.session_state.chat_history.append(chatbot_message)

    else:
        st.write("Please upload a PDF file to start the chatbot.")
