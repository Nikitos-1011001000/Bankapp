def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты"""
    digits = card_number.replace(" ", "")
    if not digits.isdigit() or len(digits) < 10:
        return ""

    stars_count = len(digits) - 8
    return digits[:4] + "*" * stars_count + digits[-4:]


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета"""
    digits = account_number.replace(" ", "")

    if len(digits) < 8:
        return ""

    masked = digits[:4] + "*" * (len(digits) - 8) + digits[-4:]
    return masked
