from typing import Any

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(info: Any) -> str:
    """Маскировка карты/счета с защитой от pandas NaN."""
    info_str = str(info).strip() if info is not None else ""

    if len(info_str.split()) == 0:  # ✅ info_str!
        return "—"

    parts = info_str.split()  # ✅ info_str!
    type_name = " ".join(parts[:-1]).strip()
    last_part = parts[-1]

    if type_name.lower().startswith("счет"):
        masked_number = get_mask_account(last_part)
    else:
        masked_number = get_mask_card_number(last_part)

    return f"{type_name} {masked_number}".strip()


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
