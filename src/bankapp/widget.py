from .masks import (get_mask_account,  # импорт функций из другого модуля
                   get_mask_card_number)


def mask_account_card(info: str):
    """Функция, которая маскирует номер карты и счета."""
    digits = ''.join(re.findall(r'\d', info))
    parts = info.split()

    number = parts[-1]

    type_name = ' '.join(parts[:-1])

    if type_name.lower().startswith('счет'):

        masked_number = get_mask_account(digits)

    else:
        masked_number = get_mask_card_number(digits)

    return f"{type_name} {masked_number}"


def get_date(date_str: str):
    """Функция для замены даты"""
    date_part = date_str.split('T')[0]

    date_obj = datetime.strptime(date_part, '%Y-%m-%d').date()

    return date_obj
