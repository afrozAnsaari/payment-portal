import streamlit as st

from api import login, register


def show_auth():

    st.title("💳 Secure Pay")
    st.caption("Fast, Secure & Smart Payments")

    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "Login"

    mode = st.radio(
        "Authentication Mode",
        ["Login", "Register"],
        horizontal=True,
        key="auth_mode",
        label_visibility="hidden",
    )

    # ================= LOGIN ================= #

    if mode == "Login":

        st.subheader("Login")

        mobile = st.text_input(
            "Mobile Number",
            key="login_mobile",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        login_button = st.button(
            "Login",
            use_container_width=True,
        )

        if login_button:

            if not mobile or not password:
                st.warning("Please enter both mobile number and password.")

            else:

                with st.spinner("Logging in..."):

                    response = login(
                        mobile,
                        password,
                    )

                if response.status_code == 200:

                    data = response.json()

                    st.write(data)

                    st.session_state["token"] = data["access_token"]

                    st.session_state.pop("login_password", None)

                    # st.write(st.session_state)

                    st.success("🎉 Login Successful!")

                    # st.stop()

                    st.rerun()

                else:

                    try:
                        detail = response.json()["detail"]

                    except Exception:
                        detail = "Login failed."

                    st.error(detail)

    # ================= REGISTER ================= #

    else:

        st.subheader("Create Account")

        name = st.text_input(
            "Full Name",
            key="register_name",
        )

        mobile = st.text_input(
            "Mobile Number",
            key="register_mobile",
        )

        email = st.text_input(
            "Email",
            key="register_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password",
        )

        register_button = st.button(
            "Register",
            use_container_width=True,
        )

        if register_button:

            if not all([name, mobile, email, password]):
                st.warning("Please fill all the fields.")

            else:

                user_data = {
                    "name": name,
                    "mobile_no": mobile,
                    "email": email,
                    "password": password,
                }

                with st.spinner("Creating Account..."):

                    response = register(user_data)

                if response.status_code in (200, 201):

                    st.info(
                        "Registration successfull. Please click on **Login** above and sign in with your new account."
                    )

                    # Clear registration form
                    st.session_state.pop("register_name", None)
                    st.session_state.pop("register_mobile", None)
                    st.session_state.pop("register_email", None)
                    st.session_state.pop("register_password", None)

                else:
                    # st.write(response.json())

                    try:
                        error = response.json()

                        if isinstance(error["detail"], list):
                            detail = error["detail"][0]["msg"]
                            detail = detail.replace("Value error, ", "")
                        else:
                            detail = error["detail"]

                    except Exception:
                        detail = "Registration failed. Please try again later."

                    st.error(detail)
