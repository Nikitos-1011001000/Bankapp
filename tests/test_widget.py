import datetime
import os
import sys
from typing import Any

import pytest

from src.bankapp.masks import get_mask_account
from src.bankapp.widget import get_date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(
    params=[
        ("1234567890123456", "1234********3456", False),  # карта 16 цифр
        ("1234 5678 9012 3456", "1234********3456", False),  # карта с пробелами
        ("1234567890123456789", "1234***********6789", False),  # карта 19 цифр
        ("1234567890", "1234**7890", False),  # счет 10 символов
        ("1234567", "1234567", False),  # короткий счет
        ("AB12CD34EF56GH78", "AB12********GH78", False),  # альфа-карта
        ("!!!invalid!!!", None, True),  # некорректный ввод
        ("", "", False),  # пустая строка
    ]
)
def example_numbers(request) -> Any:
    return request.param


@pytest.fixture
def expected_output(input_number):
    return input_number[1]


@pytest.fixture
def expect_error(input_number):
    return input_number[2]


@pytest.mark.parametrize(
    "input_number, expected_output",
    [
        ("1234567890123456", "1234********3456"),
        ("1234567", "1234567"),
        ("", ""),
        ("1234567890", "1234**7890"),
        ("ABCD1234EFGH5678", "ABCD********5678"),
    ],
)
def test_mask_account(input_number, expected_output):
    result = get_mask_account(input_number)
    assert result == expected_output


@pytest.fixture(
    params=[
        ("2024-12-31", datetime.datetime(2024, 12, 31).date()),
        ("31.12.2024", datetime.datetime(2024, 12, 31).date()),
        # Американский формат с косой чертой
        ("12/31/2024", datetime.datetime(2024, 12, 31).date()),
        ("2024/12/31", None),  # Нестандартный формат
        ("", None),  # Пустая строка
        (None, None),  # None вместо строки
        ("random string", None),
    ]
)
def test_get_date(dates):
    input_str, expected_date = dates
    assert get_date(input_str) == expected_date


@pytest.fixture(
    params=[
        ("2024-12-31", datetime.datetime(2024, 12, 31).date()),  # ISO формат
        ("31.12.2024", datetime.datetime(2024, 12, 31).date()),
        # Американский формат с косой чертой
        ("12/31/2024", datetime.datetime(2024, 12, 31).date()),
        ("2024/12/31", None),  # Нестандартный формат
        ("", None),  # Пустая строка
        (None, None),  # None вместо строки
        ("random string", None),  # Некорректная строка
    ]
)
def example_dates(request):
    return request.param


def test_mask_account_edge_cases():
    """Дополнительные edge-кейсы для widget."""
    from src.bankapp.masks import get_mask_account
    assert get_mask_account("123") == "123"  # ✅ короткие как есть
    assert get_mask_account("") == ""


def test_mask_account_card_full():
    """Полное покрытие widget.py."""
    from src.bankapp.widget import mask_account_card
    assert mask_account_card("2848284828482848") == "2848********2848"
