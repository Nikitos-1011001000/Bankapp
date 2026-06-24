import json
import logging
import os
from typing import Any, Dict, List

utils_logger = logging.getLogger("utils")


def load_transactions(filename: str = "data/transactions.csv") -> List[dict]:
    """
    Загружает транзакции ИЗ data/operations.json.
    Returns:
        List[Dict[str, Any]]: Список транзакций
        или пустой список при ошибке
    """
    json_path: str = "data/operations.json"

    utils_logger.info("Загрузка транзакций из data/operations.json")

    # Файл не найден
    if not os.path.exists(json_path):
        utils_logger.warning("⚠️ Файл data/operations.json не найден")
        return []

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data: list[Dict[str, Any]] = json.load(file)

        # Проверяем, что это список
        if not isinstance(data, list):
            utils_logger.warning("⚠️ Файл содержит не список, а другой тип данных")
            return []

        # Проверяем, что элементы — словари
        if not all(isinstance(item, dict) for item in data):
            utils_logger.warning("⚠️ Элементы в файле не все словари")
            return []

        utils_logger.info(f"✅ Загружено {len(data)} транзакций успешно")
        return data  # type: ignore[return-value]

    except (json.JSONDecodeError, PermissionError) as e:
        # Некорректный JSON или проблемы с доступом
        print(f"Ошибка загрузки {json_path}: {e}")  # type: ignore[untyped-call]
        utils_logger.error(f"❌ Ошибка загрузки {json_path}: {e}")
        return []


class CurrencyConverter:
    """Конвертер валют для тестов."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    def get_rub_amount(self, transaction: dict) -> float:
        """Mock для тестов."""
        return 100.0  # Заглушка
