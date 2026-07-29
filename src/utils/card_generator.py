from datetime import datetime

from src.config.card_bins import BANK_BINS
from src.utils.luhn import calculate_check_digit


def generate_card_number(
    bank_name: str,
    network: str,
    account_id: int,
) -> str:

    bin_number = BANK_BINS[bank_name.upper()][network.upper()]

    account_identifier = str(account_id).zfill(9)

    base_number = bin_number + account_identifier

    check_digit = calculate_check_digit(base_number)

    return base_number + check_digit


def generate_expiry():
    now = datetime.now()

    return (
        now.month,
        now.year + 5,
    )
