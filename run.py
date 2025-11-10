# import streamlit as st
#
# about_page =st.Page(
#     page="views/about_me.py",
#     title="About Me",
#     icon =":material/account_circle:",
#     default=True,
# )
# project_1_page=st.Page(
#     page="views/sales_dashboard.py",
#     title="Sales Dashboard",
#     icon=":material/bar_chart:",
#
# )
#
# project_2_page=st.Page(
#     page="views/chatbot.py",
#     title="Chat Bot",
#     icon=":material/smart_toy:",
#
# )
#
# pg=st.navigation(
#     {
#         "Info" : [about_page],
#         "Projects": [project_1_page,project_2_page],
#     },
#     # },pages=[about_page, project_1_page, project_2_page])
# )
#
# st.logo("assets/c.gif", )
# st.sidebar.text("Made with ❤️ by Aditya")
# pg.run()


import streamlit as st

# --- Define your pages ---
about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True,
)

project_1_page = st.Page(
    page="views/sales_dashboard.py",
    title="Sales Dashboard",
    icon=":material/bar_chart:",
)

project_2_page = st.Page(
    page="views/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
)

# --- Set up navigation ---
pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_1_page, project_2_page],
    }
)

# --- Optional: Add branding and sidebar content ---
st.logo("assets/c.gif")
st.sidebar.text("Made with ❤️ by Aditya")

# --- Run the selected page ---
pg.run()
