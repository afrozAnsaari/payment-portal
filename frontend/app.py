import streamlit as st

from auth import show_auth
from components.sidebar import sidebar

# Page imports
from screens.dashboard import show_dashboard
from screens.send_money import show_send_money
from screens.history import show_history
# from screens.profile import show_profile
from screens.link_bank import show_link_bank
from screens.upi_profile import show_upi_profile

st.set_page_config(
    page_title="Secure Pay",
    page_icon="💳",
    layout="wide",
)


# selected = sidebar()

# st.write(selected)

# st.write(st.session_state)


if "token" not in st.session_state:
    show_auth()

else:

    selected = sidebar()

    if selected == "Dashboard":
        show_dashboard()

    elif selected == "Send Money":
        show_send_money()

    elif selected == "History":
        show_history()

    # elif selected == "Profile":
    #     show_profile()

    elif selected == "Logout":
        st.session_state.clear()
        st.rerun()
    elif selected == "Add Profile":
        show_upi_profile()

    elif selected == "Link Bank Account":
        show_link_bank()
