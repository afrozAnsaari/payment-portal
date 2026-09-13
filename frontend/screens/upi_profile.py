import streamlit as st

from api import (
    get_upi_profile,
    create_upi_profile,
)


def show_upi_profile():

    st.title("UPI Profile")

    token = st.session_state["token"]

    # --------------------------------------------------
    # Fetch existing UPI Profile
    # --------------------------------------------------

    response = get_upi_profile(token)

    if response.status_code != 200:

        try:
            detail = response.json().get(
                "detail",
                "Unable to fetch your UPI Profile.",
            )
        except Exception:
            detail = "Unable to fetch your UPI Profile."

        st.error(detail)

        return

    profile = response.json()

    # ==================================================
    # Existing UPI Profile
    # ==================================================

    if profile["exists"]:

        st.success("UPI Profile Found")

        st.write(f"**UPI ID:** {profile['upi_id']}")

        st.write("UPI Profile Status: Active")

        return

    # ==================================================
    # No UPI Profile
    # ==================================================

    st.warning("You don't have a UPI Profile yet.")

    st.subheader("Create your UPI Profile")

    # --------------------------------------------------
    # Use a form so all fields are submitted together
    # --------------------------------------------------

    with st.form(key="create_upi_profile_form"):

        upi_id = st.text_input(
            "UPI ID",
            placeholder="example@gpay.com",
        )

        upi_pin = st.text_input(
            "UPI PIN",
            type="password",
            placeholder="Enter 4-6 digit UPI PIN",
        )

        confirm_upi_pin = st.text_input(
            "Confirm UPI PIN",
            type="password",
            placeholder="Re-enter your UPI PIN",
        )

        create_button = st.form_submit_button(
            "Create UPI Profile",
            use_container_width=True,
        )

    # ==================================================
    # Handle form submission
    # ==================================================

    if not create_button:
        return

    # --------------------------------------------------
    # Validate UPI ID
    # --------------------------------------------------

    if not upi_id.strip():

        st.warning("Please enter a UPI ID.")

        return

    # --------------------------------------------------
    # Validate UPI PIN
    # --------------------------------------------------

    if not upi_pin.strip():

        st.warning("Please enter a UPI PIN.")

        return

    # --------------------------------------------------
    # Validate confirmation PIN
    # --------------------------------------------------

    if not confirm_upi_pin.strip():

        st.warning("Please confirm your UPI PIN.")

        return

    # --------------------------------------------------
    # Make sure both PINs match
    # --------------------------------------------------

    if upi_pin != confirm_upi_pin:

        st.error("UPI PINs do not match.")

        return

    # --------------------------------------------------
    # Make sure PIN contains only digits
    # --------------------------------------------------

    if not upi_pin.isdigit():

        st.error("UPI PIN must contain only digits.")

        return

    # --------------------------------------------------
    # Validate PIN length
    # --------------------------------------------------

    if not (4 <= len(upi_pin) <= 6):

        st.error("UPI PIN must be between 4 and 6 digits.")

        return

    # ==================================================
    # Create UPI Profile
    # ==================================================

    with st.spinner("Creating UPI Profile..."):

        create_response = create_upi_profile(
            token=token,
            upi_id=upi_id.strip(),
            upi_pin=upi_pin,
        )

    # ==================================================
    # Handle API response
    # ==================================================

    if create_response.status_code in (200, 201):

        st.success("UPI Profile created successfully.")

        st.rerun()

    else:

        try:

            detail = create_response.json().get(
                "detail",
                "Unable to create UPI Profile.",
            )

        except Exception:

            detail = "Unable to create UPI Profile."

        st.error(detail)
