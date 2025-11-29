import pytest

from bankapp.masks import get_mask_card_number
from bankapp.masks import get_mask_account

@pytest.fixture
def card_numbers():
    return [
        ("1234567890123456", "1234********3456"),  # обычный 16-значный номер
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

@pytest.mark.parametrize("short_card", ["", "123", "12345678"])
def test_get_mask_card_number_short(short_card):
    with pytest.raises(ValueError):
        get_mask_card_number(short_card)

@pytest.fixture
def invalid_card_numbers():
        return [
                "",  # 0 цифр
                "1234567",  # 7 цифр
                "12345678",  # 8 цифр
                "ABCD1234EFGH5678",  # буквы + 8 цифр
            ]

def test_get_mask_card_number_valid(valid_card_numbers):
        for card, expected in valid_card_numbers:
        assert get_mask_card_number(card) == expected

@pytest.mark.parametrize("invalid_card", invalid_card_numbers)
def test_get_mask_card_number_invalid(invalid_card):
        with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)

def test_get_mask_account(account_numbers):
    for account, expected in account_numbers:
    assert get_mask_account(account) == expected
