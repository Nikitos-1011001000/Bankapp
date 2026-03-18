from .masks_logger import masks_logger


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты"""
    masks_logger.info(f"🔧 Маскировка карты: {card_number[:4]}****{card_number[-4:]}")

    digits = card_number.replace(" ", "")
    if not digits.isdigit() or len(digits) < 10:
        masks_logger.error("❌ Карта невалидна: не цифры или <10 символов")
        return ""

    stars_count = len(digits) - 8
    masks_logger.info("✅ Карта замаскирована")
    return digits[:4] + "*" * stars_count + digits[-4:]


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета"""
    masks_logger.info(f"🔧 Маскировка счета: {account_number[:4]}****{account_number[-4:]}")
    digits = account_number.replace(" ", "")

    if len(digits) < 8:
        masks_logger.error("❌ Счет невалиден: <8 символов")
        return ""

    masked = digits[:4] + "*" * (len(digits) - 8) + digits[-4:]
    masks_logger.info(f"✅ Счет замаскирован: {masked}")
    return masked
