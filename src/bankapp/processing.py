from typing import Dict, List  # ← Добавь в начало!


def filter_by_state(
    records: List[Dict[str, str]], state: str = "EXECUTED"  # ← str значения!
) -> List[Dict[str, str]]:  # ← Возвращает тот же тип!
    """Фильтрует список словарей по значению ключа 'state'."""
    return [record for record in records if record.get("state") == state]


def sort_by_date(
    records: List[Dict[str, str]], descending: bool = False  # ← str значения!
) -> List[Dict[str, str]]:  # ← Возвращает тот же тип!
    def get_date(record: Dict[str, str]) -> str:
        return record.get("date") or ""

    """Сортирует по дате."""
    return sorted(records, key=get_date, reverse=descending)
