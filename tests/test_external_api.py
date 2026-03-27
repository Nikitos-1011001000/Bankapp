import os
import sys
import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

from src.bankapp.external_api import get_rub_amount

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestCurrencyConverter(unittest.TestCase):

    def test_rub_amount(self) -> None:
        """RUB транзакция — без конвертации."""
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "1000.00", "currency": {"code": "RUB", "name": "Российский рубль"}}
        }
        result: float = get_rub_amount(transaction)
        self.assertEqual(result, 1000.0)

    @patch("external_api.os.getenv")
    def test_no_api_key(self, mock_getenv: MagicMock) -> None:
        """Нет API ключа — возвращаем исходную сумму."""
        mock_getenv.return_value = None

        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "100.50", "currency": {"code": "USD", "name": "US Dollar"}}
        }
        result: float = get_rub_amount(transaction)
        self.assertEqual(result, 100.50)

    @patch("external_api.os.getenv")
    @patch("external_api.requests.get")
    def test_usd_to_rub_success(self, mock_get: MagicMock, mock_getenv: MagicMock) -> None:
        """USD→RUB конвертация успешна."""
        mock_getenv.return_value = "fake_key"
        mock_response: Mock = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 90.5}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "US Dollar"}}
        }
        result: float = get_rub_amount(transaction)
        self.assertEqual(result, 9050.0)  # 100 * 90.5
        mock_get.assert_called_once()

    @patch("external_api.os.getenv")
    @patch("external_api.requests.get")
    def test_api_error(self, mock_get: MagicMock, mock_getenv: MagicMock) -> None:
        """API ошибка — исходная сумма."""
        mock_getenv.return_value = "fake_key"
        mock_get.side_effect = Exception("Network error")

        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "50.25", "currency": {"code": "EUR", "name": "Euro"}}
        }
        result: float = get_rub_amount(transaction)
        self.assertEqual(result, 50.25)

    @patch("external_api.os.getenv")
    def test_template_key(self, mock_getenv: MagicMock) -> None:
        """Шаблонный ключ — исходная сумма."""
        mock_getenv.return_value = "your_api_key_here"

        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "200.75", "currency": {"code": "GBP", "name": "Pound Sterling"}}
        }
        result: float = get_rub_amount(transaction)
        self.assertEqual(result, 200.75)


if __name__ == "__main__":
    unittest.main()
