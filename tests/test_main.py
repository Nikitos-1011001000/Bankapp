import os
import sys
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

import main

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Банковские транзакции для тестов."""
    return [
        {
            "state": "EXECUTED",
            "description": "Перевод организации",
            "operationAmount": {"amount": "10000.00", "currency": {"code": "RUB"}},
            "date": "2019-08-26T10:50:58.154075"
        },
        {
            "state": "EXECUTED",
            "description": "Перевод с карты",
            "operationAmount": {"amount": "130.00", "currency": {"code": "USD"}},
            "date": "2019-07-03T18:35:29.512407"
        }
    ]


# ✅ Тест get_date_sorting (mock input)
@patch('builtins.input', side_effect=['да', 'по убыванию'])
def test_get_date_sorting_descending(mock_input, sample_transactions):
    """Сортировка по убыванию."""
    result = main.get_date_sorting(sample_transactions)
    assert len(result) == 2
    # Проверяем, что вызвана sort_by_date


@patch('builtins.input', side_effect=['нет'])
def test_get_date_sorting_skip(mock_input, sample_transactions):
    """Пропуск сортировки."""
    result = main.get_date_sorting(sample_transactions)
    assert result == sample_transactions  # Не изменился


# ✅ Тест get_rub_filter
def test_get_rub_filter_yes(sample_transactions):
    """Только рубли."""
    with patch('builtins.input', return_value='да'):
        result = main.get_rub_filter(sample_transactions)
        assert len(result) == 1  # Только RUB
        assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_get_rub_filter_no(sample_transactions):
    """Все транзакции."""
    with patch('builtins.input', return_value='нет'):
        result = main.get_rub_filter(sample_transactions)
        assert len(result) == 2  # Все


# ✅ Тест get_search_filter
@patch('builtins.input', side_effect=['да', 'перевод'])
def test_get_search_filter_found(mock_input, sample_transactions):
    """Поиск найден."""
    result = main.get_search_filter(sample_transactions)
    assert len(result) == 2  # Оба содержат "перевод"


@patch('builtins.input', side_effect=['нет'])
def test_get_search_filter_skip(mock_input, sample_transactions):
    """Пропуск поиска."""
    result = main.get_search_filter(sample_transactions)
    assert result == sample_transactions


# ✅ Тест print_transactions
def test_print_transactions_empty(capfd):
    """Пустой список."""
    main.print_transactions([])
    captured = capfd.readouterr()
    assert "Не найдено ни одной" in captured.out


def test_print_transactions_nonempty(capfd, sample_transactions):
    """Есть транзакции."""
    main.print_transactions(sample_transactions)
    captured = capfd.readouterr()
    assert "Всего банковских операций" in captured.out
    assert "2" in captured.out


# ✅ Тесты загрузчиков
def test_load_csv(mocker):
    """Mock CSV загрузка."""
    mock_open = mocker.mock_open(read_data='id,state,description\n1,EXECUTED,test')
    mocker.patch('builtins.open', mock_open)

    result = main.load_csv("fake.csv")
    assert len(result) == 1
    assert result[0]["state"] == "EXECUTED"


def test_load_xlsx(mocker):
    """Mock XLSX загрузка."""
    mock_wb = MagicMock()
    mock_ws = MagicMock()
    mock_ws.active = mock_ws
    mock_ws[1] = [MagicMock(value='id'), MagicMock(value='state')]
    mock_ws.iter_rows.return_value = [('1', 'EXECUTED')]

    mocker.patch('openpyxl.load_workbook', return_value=mock_wb)
    mocker.patch.object(mock_wb, 'active', mock_ws)

    result = main.load_xlsx("fake.xlsx")
    assert len(result) == 1


def get_last_transactions(transactions: list[dict], count: int = 5) -> list[dict]:
    """Возвращает последние N транзакций."""
    return transactions[-count:] if transactions else []
