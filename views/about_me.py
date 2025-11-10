import streamlit as st

# ✅ Use the new dialog API
@st.dialog("Contact Me")
def show_contact_form():
    st.text_input("First Name")
    st.text_input("Last Name")
    st.text_input("Email")
    st.number_input("Phone Number")
    st.text_input("Message")
    bt = st.button("Submit 🚀")
    if bt:
        st.success("Message sent Successfully !!")


# --- Layout ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.image("./assets/s.png")

with col2:
    st.title("Aditya Bhattacharya", anchor=False)
    st.write("Aspiring Software Engineer and Developer")

    # 🖥️ Button to open dialog
    if st.button("🖥️ Contact Me"):
        show_contact_form()

st.write("\n")

# --- Info Section ---
col1, col2 = st.columns(2, gap="small")

with col1:
    st.subheader("Experience & Qualification", anchor=False)
    st.write(
        "Undergraduate student in B.Tech Computer Science, Rajiv Gandhi Institute of Petroleum Technology"
    )
    st.write(
        """
    - Strong hands-on experience and knowledge in Machine / Deep Learning, Full Stack Web / App Development
    - Good understanding of statistical principles and their respective applications
    - Excellent team-player and displaying a strong sense of initiative
    """
    )

with col2:
    st.image(
        "./views/Rajiv_Gandhi_Institute_of_Petroleum_Technology-removebg-preview.png",
        width=50,
    )
    st.subheader("Proficient in Tech Stacks:", anchor=False)
    st.image("./assets/img.png")
