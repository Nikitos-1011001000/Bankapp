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

@pytest.fixture
def valid_card_numbers():
    return [
        ("4111111111111111", "400000******1111"),  # Visa
        ("5555555555554444", "555555******4444"),  # Mastercard
        ("4111111111114555", "400000******4555"),  # Visa Classic
        ("2222400070000005", "222240******0005"),  # Mastercard Commercial
        ("4242424242424242", "400000******4242"),  # Stripe test Visa
        ("4000000000000002", "400000******0002"),  # Visa test
        ("5105105105105100", "510510******5100"),  # Mastercard test
        ("378282246310005",  "378282******005"),   # Amex
        ("6011111111111117", "601111******1117"),  # Discover
    ]

def test_get_mask_card_number_valid(valid_card_numbers):
        for card, expected in valid_card_numbers:
        assert get_mask_card_number(card) == expected

@pytest.fixture
def invalid_card_numbers():
    return [
        ("abcd-efgh-ijkl-mnop", ""),
        ("9999999999999999", ""),
    ]

@pytest.mark.parametrize("fixture_name", ["invalid_card_numbers"])
def test_get_mask_card_number_invalid(request):
    invalid_cards = request.getfixturevalue(fixture_name)
    for card in invalid_cards:
        assert get_mask_card_number(card) == ""

def test_get_mask_account(account_numbers):
    for account, expected in account_numbers:
    assert get_mask_account(account) == expected
