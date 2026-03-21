import os
import sys
import requests
from pathlib import Path
from typing import Any, Dict, Optional
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

    rate: Optional[float] = _get_exchange_rate(currency_code)
    if rate is not None:  # ✅ ПРОВЕРКА!
        return amount * rate

    return amount  # ✅ FALLBACK!


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
    except (requests.RequestException, KeyError, ValueError, Exception) as e:  # ✅ ДОБАВЬ Exception!
        print(f"Ошибка API: {e}")
        return None  # ✅ return None!


if __name__ == "__main__":
    """Демо: python -m utils.currency → тест конвертации API"""
    from bankapp.utils import \
        load_transactions  # type: ignore[import-untyped]

    print("Тестируем конвертацию валют...")
    transactions: list[Dict[str, Any]] = load_transactions()[:5]  # type: ignore[untyped-call]

    if not transactions:
        print("data/operations.json не найден или пуст!")

print("\nРезультаты конвертации:")
print("-" * 50)
