from .masks import (get_mask_account,  # импорт функций из другого модуля
                   get_mask_card_number)
import datetime


def mask_account_card(info: str):
    card_number = str(card_number)
    if len(card_number) < 8:
        return card_number
    masked_length = len(card_number) - 8
    return card_number[:4] + '*' * masked_length + card_number[-4:]


def get_date(date_str: str):
    """Функция для замены даты"""
    date_part = date_str.split('T')[0]

    date_obj = datetime.strptime(date_part, '%Y-%m-%d').date()

    return date_obj
