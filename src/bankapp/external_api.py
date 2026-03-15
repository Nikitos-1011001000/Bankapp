import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

load_dotenv()


def get_rub_amount(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли ИЗ operations.json.

    Args:
        transaction:
    Словарь из data/operations.json
    {"id": int, "state": str, "operationAmount": {...}, ...}

    Returns:
        float: Сумма в рублях
    """
    amount_info: Dict[str, Any] = transaction.get("operationAmount", {})
    amount_str: Any = amount_info.get("amount", "0.0")
    amount: float = float(amount_str)

    currency_info: Dict[str, Any] = amount_info.get("currency", {})
    currency_code: str = currency_info.get("code", "RUB").upper()

    # Уже в рублях
    if currency_code == "RUB":
        return amount

    # Конвертируем
    rate: Optional[float] = _get_exchange_rate(currency_code)
    return amount * rate if rate is not None else amount


def _get_exchange_rate(currency: str) -> Optional[float]:
    """Получает курс currency->RUB из API."""
    api_key: Optional[str] = os.getenv("EXCHANGERATES_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        print("⚠️  API ключ не настроен! Используем исходную сумму.")
        return None

    url: str = "https://api.apilayer.com/exchangerates_data/latest"
    headers: Dict[str, str] = {"apikey": api_key}
    params: Dict[str, str] = {"symbols": "RUB", "base": currency}

    try:
        response: requests.Response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        rub_rate: Optional[float] = data["rates"].get("RUB")
        return rub_rate
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Ошибка API: {e}")
        return None


if __name__ == "__main__":
    """Демо: python -m utils.currency → тест конвертации API"""
    from utils.transactions import load_transactions  # type: ignore[import-untyped]

    print("Тестируем конвертацию валют...")
    transactions: list[Dict[str, Any]] = load_transactions()[:5]  # type: ignore[untyped-call]

    if not transactions:
        print("data/operations.json не найден или пуст!")

print("\nРезультаты конвертации:")
print("-" * 50)

for tx in transactions:
    rub_amount: float = get_rub_amount(tx)
    tx_id: Any = tx.get("id", "N/A")
    currency_info: Dict[str, Any] = tx.get("operationAmount", {})
    currency: Dict[str, Any] = currency_info.get("currency", {})
    currency_code: str = currency.get("code", "N/A")

    print(f"ID {tx_id:<6} | {rub_amount:>12.2f} ₽ | {currency_code:>3}")

    print("-" * 50)
    print("Конвертация завершена!")
