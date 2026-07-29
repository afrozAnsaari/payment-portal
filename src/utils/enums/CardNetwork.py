from enum import Enum


class CardNetwork(str, Enum):

    RUPAY = "RUPAY"
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
