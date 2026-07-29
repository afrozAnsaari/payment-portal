import random






def generate_account_number() -> str:

    return str(
        random.randint(
            100000000000,
            999999999999,
        )
    )


IFSC_CODES = {
    "SBI": "SBIN00001234",
    "HDFC": "HDFC00001234",
    "ICICI": "ICICI00001234",
}


def get_ifsc_code(bank_name: str) -> str:

    return IFSC_CODES.get(
        bank_name.upper(),
        "BANK0000000",
    )
