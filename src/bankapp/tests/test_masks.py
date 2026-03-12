import pytest

from bankapp.masks import get_mask_card_number
from bankapp.masks import get_mask_account


@pytest.fixture
def card_numbers():
    return [
        ("1234567890123456", "1234********3456"),  # обычный 16-значный номер
        ("1234567890123456789", "1234***********6789"),  # 19-значный номер
    ]


def test_get_mask_card_number(card_numbers):
    for card, expected in card_numbers:
        assert get_mask_card_number(card) == expected


@pytest.fixture
def account_numbers():
    return [
        ("1234567890123456", "1234********3456"),  # обычный 16-значный номер
        ("1234567", "1234567"),  # меньше ожидаемой длины, без изменений
        ("", ""),  # пустая строка
        ("1234567890", "1234**7890"),
        ("ABCD1234EFGH5678", "ABCD********5678"),  # альфа-цифровой номер
    ]


@pytest.fixture
def invalid_card_numbers():
    return [
        "",  # 0 цифр
        "1234567",  # 7 цифр
        "12345678",  # 8 цифр
        "ABCD1234EFGH5678",  # буквы + 8 цифр
    ]


@pytest.fixture
def valid_card_numbers():
    return [
        ("4111111111111111", "4111********1111"),  # 4 вместо 6
        ("5555555555554444", "5555********4444"),  # Mastercard
        ("4000111111114555", "4000********4555"),  # Visa Classic
        ("2222400070000005", "2222********0005"),  # Mastercard Commercial
        ("4242424242424242", "4242********4242"),  # Stripe test Visa
        ("4000000000000002", "4000********0002"),  # Visa test
        ("5105105105105100", "5105********5100"),  # Mastercard test
        ("6011111111111117", "6011********1117"),  # Discover
    ]


def test_get_mask_card_number_valid(valid_card_numbers):
    for card, expected in valid_card_numbers:
        assert get_mask_card_number(card) == expected


@pytest.mark.parametrize("invalid_card", ["123", "abcd-efgh-ijkl-mnop"])
def test_get_mask_card_number_invalid(invalid_card):
    assert get_mask_card_number(invalid_card) == ""


def test_get_mask_account(account_numbers):
    for account, expected in account_numbers:
        assert get_mask_account(account) == expected
