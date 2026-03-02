def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты"""
    digits = card_number.replace(" ", "")

    if len(digits) < 10:
        raise ValueError("Неверный номер карты")

    masked = digits[:4] + " " + digits[4:6] + "** **** " + digits[-4:]
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета"""
    digits = account_number.replace(" ", "")

    if len(digits) < 4:
        raise ValueError("Неверный номер счета")

    masked = "**" + digits[-4:]
    return masked
