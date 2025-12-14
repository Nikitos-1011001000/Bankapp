def get_mask_card_number(card_number):
    # Убираем все нецифры
    clean = ''.join(c for c in str(card_number) if c.isdigit())

    # Если меньше 12 цифр - ValueError
    if len(clean) < 12 and len(clean) > 0:
        return ""


    if len(clean) == 0:
        return ""

    # Количество звездочек = общая_длина - 8 (4+4 видимых)
    stars_count = len(clean) - 8
    return clean[:4] + '*' * stars_count + clean[-4:]

def get_mask_account(account):
    account = str(account)

    # Если длина < 8 — возвращаем как есть
    if len(account) < 8:
        return account

    # Сохраняем первые 4 и последние 4 символа, маскируем середину
    masked_length = len(account) - 8
    return account[:4] + '*' * masked_length + account[-4:]