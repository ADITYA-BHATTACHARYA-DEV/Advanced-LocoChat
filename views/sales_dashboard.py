import streamlit as st

col1, col2 = st.columns(2, gap='small', vertical_alignment="center")

with col1:
    st.image("./assets/ts.png")
with col2:
    st.title("LocoChat", anchor=False)

    st.write(

        "Description & Working "
    )

st.write("\n")

with col2:
    st.title("Description", anchor=False)
    st.write(
        """
    - Powered by the formidable Llama3 Large Language Model (LLM) with  Ollama transcends mere data retrieval.
    - It embodies the fusion of cutting-edge technologies, seamlessly blending Retrieval Adversarial Generation (RAG) Pipeline with an unwavering commitment to accuracy and autonomy.
    - LocoChat isn’t just a chatbot, it’s an enigma. An AI sage that transcends the mundane, as it navigates the labyrinth of data with conjuration.
    
    """
    )

st.write("\n")
with col1:
    st.title("Working", anchor=False)
    st.subheader("The Rag Unleashed", anchor=False)
    st.write(
        """
    - 
    It’s retrieval module scours internal databases like a seasoned librarian.
    It fetches nuggets of wisdom, even from the darkest corners of data archives.
    - Ollama’s adversarial generator refines raw information.
    It transforms mundane facts into eloquent narratives, ready for human consumption.
    - The System crafts responses like a poetic alchemist.
    Its prose dances between clarity and intrigue, leaving users spellbound.
    """
    )


with col2:
    st.image("./assets/ssn.png")
