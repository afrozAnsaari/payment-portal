from streamlit_option_menu import option_menu
import streamlit as st


def sidebar():

    with st.sidebar:

        selected = option_menu(
            menu_title="Secure Pay",
            options=[
                "Dashboard",
                "Send Money",
                "History",
                "Profile",
                "Add Profile",
                "Link Bank Account",
                "Settings",
                "Logout",
            ],
            icons=[
                "house",
                "cash-stack",
                "clock-history",
                "person",
                "gear",
                "box-arrow-right",
                "person-plus",
                "bank",
            ],
            default_index=0,
            key="main_sidebar_menu"
        )

    return selected
