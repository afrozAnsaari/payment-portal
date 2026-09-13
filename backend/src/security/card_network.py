def detect_network(
    card_number: str,
) -> str:

    if card_number.startswith("4"):
        return "VISA"

    if card_number.startswith(tuple(str(i) for i in range(51, 56))):
        return "MASTERCARD"

    if card_number.startswith(("34", "37")):
        return "AMEX"

    if card_number.startswith(("60", "65")):
        return "RUPAY"

    return "UNKNOWN"


if __name__ == "__main__":
    print("Card No.:4111111111111111", detect_network("4111111111111111"))
