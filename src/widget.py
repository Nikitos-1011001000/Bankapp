def mask_account_card(info):
    """Функция, которая маскирует номер карты и счета."""

    from masks import get_mask_card_number
    from masks import get_mask_account


def get_date(date_str):
    """Функция для замены даты"""
    date_part = date_str.split('T')[0]

    year, month, day = date_part.split('-')

    return f"{day}.{month}.{year}"