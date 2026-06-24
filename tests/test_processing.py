import os
import sys
from typing import Any, Dict, List

import pytest

from src.bankapp.processing import (filter_by_state, process_bank_operations,
                                    process_bank_search, sort_by_date)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(
    params=[
        # (входной список словарей, параметр state, ожидаемый результат)
        (
            [{"state": "active"}, {"state": "inactive"}, {"state": "active"}],
            "active",
            [{"state": "active"}, {"state": "active"}],
        ),
        ([{"state": "active"}, {"state": "inactive"}], "inactive", [{"state": "inactive"}]),
        ([{"state": "active"}, {"state": "inactive"}], "pending", []),  # состояния 'pending' нет в списке
        ([], "active", []),  # пустой список
        ([{"state": None}, {"state": "active"}], None, [{"state": None}]),
    ]
)
def filter_test_data(request) -> tuple[List[Dict[str, Any]], str | None, List[Dict[str, Any]]]:
    return request.param


def test_filter_by_state(filter_test_data):
    items, state, expected = filter_test_data
    assert filter_by_state(items, state) == expected


@pytest.fixture(params=[
    (
        [{"date": "2024-01-02"}, {"date": "2023-12-31"}, {"date": "2024-01-01"}],
        True,  # descending
        [{"date": "2024-01-02"}, {"date": "2024-01-01"}, {"date": "2023-12-31"}],
    ),
    (
        [{"date": "2024-01-01"}, {"date": "2024-01-01"}, {"date": "2023-12-30"}],
        False,  # ascending
        [{"date": "2023-12-30"}, {"date": "2024-01-01"}, {"date": "2024-01-01"}],
    ),
    ([], True, []),
])
def sort_data(request):
    return request.param


def test_sort_by_date(sort_data):
    items, descending, expected = sort_data
    result = sort_by_date(items, descending)
    assert result == expected


# ✅ НОВЫЕ тесты для process_bank_search (REGEX!)
@pytest.fixture
def bank_transactions():
    return [
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Покупка кофе"}
    ]


def test_process_bank_search(bank_transactions):
    """Regex поиск работает."""
    result = process_bank_search(bank_transactions, "вклад")
    assert len(result) == 1
    assert result[0]["description"] == "Открытие вклада"

    result = process_bank_search(bank_transactions, "ПЕРЕВОД")
    assert len(result) == 1  # re.IGNORECASE!

    result = process_bank_search(bank_transactions, "xyz")
    assert len(result) == 0


# ✅ НОВЫЕ тесты для process_bank_operations
def test_process_bank_operations():
    """Подсчёт категорий."""
    transactions = [
        {"description": "Открытие вклада в Сбере"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"}
    ]

    categories = ["вклад", "перевод", "карта"]
    result = process_bank_operations(transactions, categories)

    assert result == {"вклад": 1, "перевод": 2, "карта": 0}
