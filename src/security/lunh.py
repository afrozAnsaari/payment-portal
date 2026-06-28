# Check the validity using Luhn's algorithm


def validate_card_number(
    card_number: str,
) -> bool:
    digits = []

    for digit in card_number:

        if not digit.isdigit():
            return False

        digits.append(int(digit))

    checksum = 0

    reverse_digits = digits[::-1]

    for idx, digit in enumerate(reverse_digits):

        if idx % 2 == 1:
            digit *= 2

            if digit > 9:
                digit -= 9

        checksum += digit

    return checksum % 10 == 0


if __name__ == "__main__":
    print("Card no.:4111111111111111", validate_card_number("4111111111111111"), "\n")
    print("Card no.:41111111111111112", validate_card_number("4111111111111112"), "\n")
