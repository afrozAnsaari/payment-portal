from cryptography.fernet import Fernet


def main():
    print("Hello from fraud-detection!")


print(Fernet.generate_key().decode())
if __name__ == "__main__":
    main()
