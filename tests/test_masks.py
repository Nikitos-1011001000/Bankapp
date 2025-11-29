import pytest

from bankapp.masks import get_mask_card_number
from bankapp.masks import get_mask_account


@pytest.fixture
def card_numbers():
    return [
        ("1234567890123456", "1234********3456"),  # обычный 16-значный номер
        ("12345678", "12345678"),                 # минимальная длина 8, не маскируется
        ("", ""),                                # пустая строка
        ("1234567", "1234567"),                   # меньше 8 символов, без изменений
        ("1234567890123456789", "1234***********6789")  # 19-значный номер
    ]

def test_get_mask_card_number(card_numbers):
    for card, expected in card_numbers:
        assert get_mask_card_number(card) == expected

@pytest.fixture
def account_numbers():
    return [
        ("1234567890123456", "1234********3456"),  # обычный 16-значный номер
        ("1234 5678 9012 3456", "1234********3456"),
        ("1234567", "1234567"),  # меньше ожидаемой длины, без изменений
        ("", ""),  # пустая строка
        ("1234567890", "1234**7890"),
        ("ABCD1234EFGH5678", "ABCD********5678"),  # альфа-цифровой номер
    ]

def test_get_mask_account(account_numbers):
    for account, expected in account_numbers:
        assert get_mask_account(account) == expected
