import requests

BASE_URL = "http://127.0.0.1:8000"


def get_headers(token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def login(mobile_no, password):
    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "mobile_no": mobile_no,
            "password": password,
        },
    )

    return response


def register(user_data):
    response = requests.post(
        f"{BASE_URL}/users/register",
        json=user_data,
    )
    return response


def get_upi_profile(token):
    response = requests.get(
        f"{BASE_URL}/upi/get-profile",
        headers=get_headers(token),
    )

    return response


def create_upi_profile(token: str, upi_id: str, upi_pin: str):

    response = requests.post(
        f"{BASE_URL}/upi/create-profile",
        headers=get_headers(token),
        json={
            "upi_id": upi_id,
            "upi_pin": upi_pin,
        },
    )

    return response


def link_bank_account(token, payload):

    return requests.post(
        f"{BASE_URL}/upi/link-bank",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=payload,
    )
