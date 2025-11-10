import streamlit as st

from streamlit_option_menu import option_menu
import os
import time

import streamlit as st
from streamlit_option_menu import option_menu
import os
import time

# userprompt & memory
from langchain_core.prompts import PromptTemplate
# Prompt templates & memory
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory  # type: ignore
 # memory stays in langchain

# Vector database
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings

# LLMs
from langchain_community.llms import Ollama

# Callbacks
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.callbacks.manager import CallbackManager

# PDF loading & splitting
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore



# Retrieval chain
from langchain.chains import RetrievalQA  # type: ignore


# Voice/audio
import pyttsx3
import speech_recognition as sr


# voice + audio
import pyttsx3
import speech_recognition as sr

if not os.path.exists('../pdfFiles'):
    os.makedirs('../pdfFiles')

if not os.path.exists('../vectorDB'):
    os.makedirs('../vectorDB')

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
    )

if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = Chroma(persist_directory='vectorDb',
                                          embedding_function=OllamaEmbeddings(base_url='http://localhost:11434',
                                                                              model="llama3")
                                          )

if 'llm' not in st.session_state:
    st.session_state.llm = Ollama(base_url="http://localhost:11434",
                                  model="llama3",
                                  verbose=True,
                                  callback_manager=CallbackManager(
                                      [StreamingStdOutCallbackHandler()]),
                                  )

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# User Interface

# st.set_page_config(page_title="LocoChat", page_icon=":eyes:")
st.header("LocoChat - Your Friendly Document Assistant", ":eyes:")


# Create a radio button group for navigation

def multipage_menu(caption):
    st.sidebar.title(caption)
    st.sidebar.subheader('Navigation')
    st.sidebar.image('assets/ss.png')


# Date Input
# date = st.sidebar.date_input('Present Date', datetime.today())

# # Time Input
# time = st.sidebar.time_input('Current Time', datetime.now().time())
#     # Add other menu items here


multipage_menu("LocoChat")
# page = st.sidebar.radio("Navigate", ["Home", "About", "Contact"])

# if page == "Home":
#     st.write("Welcome to the Home page!")
#     # Add other content specific to the Home page
# elif page == "About":
#     st.write("This is the About page.")
#     # Add other content specific to the About page
# elif page == "Contact":
#     st.write("Contact us here.")
#     # Add other content specific to the Contact page

selected = option_menu(
    menu_title="Main Menu",
    options=["Home", "History", "Contact"],
    icons=["house", "book", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",

)
# if selected == "Home":
#    st.title(f"You have selected {selected}")
# if selected == "Projects":
#    st.title(f"You have selected {selected}")
# if selected == "Contact":
#    st.title(f"You have selected {selected}")

col1, col2 = st.columns(2, gap='small', vertical_alignment="center")

with col1:
    st.image("./assets/robot-lunch.gif")
with col2:
    st.title(

        "What can I do for You?"
    )

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])

if uploaded_file is not None:
    st.text("File uploaded successfully")
    if not os.path.exists('pdfFiles/' + uploaded_file.name):
        with st.status("Saving file..."):
            bytes_data = uploaded_file.read()
            f = open('pdfFiles/' + uploaded_file.name, 'wb')
            f.write(bytes_data)
            f.close()

            loader = PyPDFLoader('pdfFiles/' + uploaded_file.name)
            data = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=200,
                length_function=len
            )

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
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        chatbot_message = {"role": "assistant", "message": response['result']}
        st.session_state.chat_history.append(chatbot_message)


else:
    st.write("Please upload a PDF file to start the chatbot")