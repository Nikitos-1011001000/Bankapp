def mask_account_card(info):
    """Функция, которая маскирует номер карты и счета."""
    parts = info.split()

    number = parts[-1]

    type_name = ' '.join(parts[:-1])

    if type_name.lower().startswith('счет'):

        masked_number = '*' * (len(number) - 4) + number[-4:]
    else:

        masked_number = number[:6] + '*' * (len(number) - 10) + number[-4:]

    return f"{type_name} {masked_number}"

def get_date(date_str):
    """Функция для замены даты"""
    date_part = date_str.split('T')[0]

    year, month, day = date_part.split('-')

    return f"{day}.{month}.{year}"