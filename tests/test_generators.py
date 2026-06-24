import os  # noqa:
import sys

from src.bankapp.generators import (card_number_generator, filter_by_currency,
                                    transaction_descriptions)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Тесты для filter_by_currency
def test_filter_by_currency_basic():
    transactions = [
        {"currency": "USD", "amount": 100},
        {"currency": "EUR", "amount": 150},
        {"currency": "USD", "amount": 50},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert all(tx["currency"] == "USD" for tx in result)


def test_filter_by_currency_no_match():
    transactions = [{"currency": "GBP", "amount": 200}]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_filter_by_currency_empty():
    assert list(filter_by_currency([], "USD")) == []


# Тесты для card_number_generator
def test_card_number_generator_small_range():
    gen = card_number_generator("0000 0000 0000 0001", "0000 0000 0000 0003")
    result = list(gen)
    expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    assert result == expected


def test_card_number_generator_format():
    gen = card_number_generator("0000 0000 0000 9998", "0000 0000 0000 9999")
    for card in gen:
        assert len(card) == 19  # 16 digits + 3 spaces
        assert card[4] == " "
        assert card[9] == " "
        assert card[14] == " "


# Тесты для transaction_descriptions
def test_transaction_descriptions_basic():
    transactions = [{"id": 1, "amount": 100, "currency": "USD"}, {"id": 2, "amount": 50, "currency": "EUR"}]
    gen = transaction_descriptions(transactions)
    descriptions = list(gen)
    assert descriptions == ["Транзакция 1: 100 USD", "Транзакция 2: 50 EUR"]


def test_transaction_descriptions_missing_keys():
    transactions = [{"amount": 100}]
    gen = transaction_descriptions(transactions)
    descriptions = list(gen)
    assert descriptions == ["Транзакция N/A: 100 N/A"]


def test_transaction_descriptions_empty():
    assert list(transaction_descriptions([])) == []
