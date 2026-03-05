from masks import (get_mask_account,  # импорт функций из другого модуля
                   get_mask_card_number)


def mask_account_card(info: str):
    """Функция, которая маскирует номер карты и счета."""
    parts = info.split()

    number = parts[-1]

    type_name = ' '.join(parts[:-1])

    if type_name.lower().startswith('счет'):

        masked_number = get_mask_account(info)

    else:
        masked_number = get_mask_card_number(info)

    return f"{type_name} {masked_number}"


def get_date(date_str: str):
    """Функция для замены даты"""
    date_part = date_str.split('T')[0]

    year, month, day = date_part.split('-')

    return f"{day}.{month}.{year}"
