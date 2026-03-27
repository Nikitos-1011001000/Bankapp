from .masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Функция, которая маскирует номер карты и счета."""
    if len(info.strip().split()) == 0:  # ← "Есть коробки?"
        return "—"
    parts = info.split()
    return get_mask_card_number(parts[-1])

    type_name = " ".join(parts[:-1])

    if type_name.lower().startswith("счет"):

        masked_number = get_mask_account(info)

    else:
        masked_number = get_mask_card_number(info)

    return f"{type_name} {masked_number}"


def get_date(date_str: str) -> str:
    """Функция для замены даты"""
    date_part = date_str.split("T")[0]

    year, month, day = date_part.split("-")

    return f"{day}.{month}.{year}"


def test_print_transactions():
    from src.bankapp.widget import print_transactions
    transactions = [{"id": 1}]
    result = print_transactions(transactions)
    assert result is None  # print возвращает None
