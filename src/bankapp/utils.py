import json
import os
from typing import Any, Dict, List


def load_transactions() -> List[Dict[str, Any]]:
    """
    Загружает транзакции ИЗ data/operations.json.
    Returns:
        List[Dict[str, Any]]: Список транзакций
        или пустой список при ошибке
    """
    json_path: str = "data/operations.json"

    # Файл не найден
    if not os.path.exists(json_path):
        return []

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data: Any = json.load(file)

        # Проверяем, что это список
        if not isinstance(data, list):
            return []

        # Проверяем, что элементы — словари
        if not all(isinstance(item, dict) for item in data):
            return []

        return data  # type: ignore[return-value]

    except (json.JSONDecodeError, PermissionError) as e:
        # Некорректный JSON или проблемы с доступом
        print(f"Ошибка загрузки {json_path}: {e}")  # type: ignore[untyped-call]
        return []


if __name__ == "__main__":
    """Запуск модуля напрямую: python -m utils.transactions"""
    transactions: List[Dict[str, Any]] = load_transactions()
    print(f"Загружено {len(transactions)} транзакций из data/operations.json")
