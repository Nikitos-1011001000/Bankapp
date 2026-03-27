import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List  # ← Добавь в начало!


def filter_by_state(
    records: List[Dict[str, str]], state: str = "EXECUTED"  # ← str значения!
) -> List[Dict[str, str]]:  # ← Возвращает тот же тип!
    """Фильтрует список словарей по значению ключа 'state'."""
    return [record for record in records if record.get("state") == state]


def sort_by_date(
    records: List[Dict[str, str]], descending: bool = False  # ← str значения!
) -> List[Dict[str, str]]:  # ← Возвращает тот же тип!
    def get_date(record: Dict[str, str]) -> datetime:
        date_str = record.get("date", "")
        if 'T' in date_str:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        return datetime.strptime(date_str, "%Y-%m-%d")

    """Сортирует по дате."""
    return sorted(records, key=get_date, reverse=descending)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Ищет строку в description с помощью re."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [tx for tx in data if pattern.search(tx.get('description', ''))]


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Считает операции по категориям в description."""
    counter = Counter({cat: 0 for cat in categories})
    for tx in data:
        desc = tx.get('description', '').lower()
        for cat in categories:
            if cat.lower() in desc:
                counter[cat] += 1  # ← Counter метод! ✓
                break
    return dict(counter)
