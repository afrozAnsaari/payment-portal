import os

from cryptography.fernet import Fernet

from dotenv import load_dotenv

load_dotenv()

# print(os.getenv("ENCRYPTION_KEY"))

cipher = Fernet(os.getenv("ENCRYPTION_KEY").encode())


def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()


def decrypt_data(data: str) -> str:

    return cipher.decrypt(data.encode()).decode()
