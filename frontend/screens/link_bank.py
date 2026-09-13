import streamlit as st

from datetime import datetime

from api import (
    get_upi_profile,
    link_bank_account,
)


def show_link_bank():

    st.title("Link Bank Account")

    token = st.session_state["token"]

    # -------------------------------------------------------
    # Fetch user's UPI Profile
    # -------------------------------------------------------

    profile_response = get_upi_profile(token)

    if profile_response.status_code != 200:

        try:
            detail = profile_response.json().get(
                "detail",
                "Unable to fetch your UPI Profile.",
            )
        except Exception:
            detail = "Unable to fetch your UPI Profile."

        st.error(detail)

        return

    profile = profile_response.json()

    # -------------------------------------------------------
    # A UPI Profile is required before linking a bank account
    # -------------------------------------------------------

    if not profile["exists"]:

        st.warning("You don't have a UPI Profile yet.")

        st.info("Create a UPI Profile first, then link your bank account.")

        return

    # =======================================================
    # USER HAS A UPI PROFILE
    # =======================================================

    st.success("UPI Profile Found")

    st.write(f"**UPI ID:** {profile['upi_id']}")

    st.divider()

    st.subheader("Link Bank Account")

    # -------------------------------------------------------
    # Bank Name
    # -------------------------------------------------------


    bank_name = st.selectbox(
        "Bank",
        [
            "SBI",
            "HDFC",
            "ICICI",
            "Axis",
            "Kotak",
        ],
    )

    # -------------------------------------------------------
    # Card Number
    # -------------------------------------------------------

    card_number = st.text_input(
        "Card Number",
        placeholder="Enter your card number",
    )

    # -------------------------------------------------------
    # Expiry Month
    # -------------------------------------------------------

    expiry_month = st.number_input(
        "Expiry Month",
        min_value=1,
        max_value=12,
        step=1,
        value=1,
    )

    # -------------------------------------------------------
    # Expiry Year
    # -------------------------------------------------------

    current_year = datetime.now().year

    expiry_year = st.number_input(
        "Expiry Year",
        min_value=current_year,
        max_value=current_year + 15,
        step=1,
        value=current_year,
    )

    # -------------------------------------------------------
    # Card PIN
    # -------------------------------------------------------

    card_pin = st.text_input(
        "Card PIN",
        type="password",
    )

    # -------------------------------------------------------
    # Link Bank Account
    # -------------------------------------------------------

    link_button = st.button(
        "Link Bank Account",
        use_container_width=True,
    )

    if not link_button:
        return

    # =======================================================
    # FRONTEND VALIDATION
    # =======================================================

    if not bank_name.strip():

        st.warning("Please enter the bank name.")

        return

    if not card_number.strip():

        st.warning("Please enter the card number.")

        return

    if not card_pin.strip():

        st.warning("Please enter the card PIN.")

        return

    # =======================================================
    # PREPARE REQUEST PAYLOAD
    # =======================================================

    payload = {
        "bank_name": bank_name.strip(),
        "card_number": card_number.strip(),
        "expiry_month": expiry_month,
        "expiry_year": expiry_year,
        "card_pin": card_pin,
    }

    # =======================================================
    # SEND REQUEST TO BACKEND
    # =======================================================

    with st.spinner("Linking Bank Account..."):

        response = link_bank_account(
            token,
            payload,
        )

    # =======================================================
    # HANDLE API RESPONSE
    # =======================================================

    if response.status_code in (200, 201):

        try:

            result = response.json()

            message = result.get(
                "message",
                "Bank account linked successfully.",
            )

        except Exception:

            message = "Bank account linked successfully."

        st.success(message)

        # Refresh the page so the latest state is loaded.
        # st.rerun()

    else:

        try:

            error_data = response.json()

            detail = error_data.get(
                "detail",
                "Unable to link bank account.",
            )

        except Exception:

            detail = "Unable to link bank account."

        st.error(detail)
