from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтр транзакций по валюте."""
    for tx in transactions:
        if tx.get("currency") == currency:
            yield tx  # Iterator, как в тестах


def card_number_generator(start: str, end: str) -> Iterator[str]:
    """Генератор номеров карт."""
    start_num = int(start.replace(" ", ""))
    end_num = int(end.replace(" ", ""))

    for num in range(start_num, end_num + 1):
        num_str = f"{num:016d}"
        formatted = " ".join(num_str[i:i + 4] for i in range(0, 16, 4))
        yield formatted


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор описаний транзакций."""
    for tx in transactions:
        # ✅ Правильный f-string
        description = f"Транзакция {tx.get('id', 'N/A')}: {tx.get('amount', 0)} {tx.get('currency', 'N/A')}"
        yield description


def get_last_transactions(transactions: List[Dict[str, Any]], count: int = 5) -> List[Dict[str, Any]]:
    """Получить последние N транзакций."""
    return transactions[-count:] if transactions else []


__all__ = ['card_number_generator', 'filter_by_currency', 'transaction_descriptions', 'get_last_transactions']
