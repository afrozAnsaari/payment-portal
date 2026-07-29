# this is a variation of luhn's algorithm that is just used to generate the check digit


def calculate_check_digit(number: str) -> str:

    digits = [int(num) for num in number]

    total = 0

    parity = (len(digits) + 1) % 2

    for idx, digit in enumerate(digits):

        if idx % 2 == parity:
            digit *= 2

            if digit > 9:
                digit -= 9
        total += digit

    return str((10 - (total % 10)) % 10)
