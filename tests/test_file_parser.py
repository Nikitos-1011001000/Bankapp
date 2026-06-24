import os
import sys
from typing import Any
from unittest.mock import MagicMock, Mock, patch

from file_parser import read_csv_transactions, read_excel_transactions

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestFileParser:
    @patch('builtins.open')
    def test_csv_file_not_found(self, mock_open: Mock) -> None:
        """Тест: CSV файл не найден."""
        mock_open.side_effect = FileNotFoundError
        result: list[dict[str, Any]] = read_csv_transactions("missing.csv")
        assert len(result) == 0

    def test_csv_success(self) -> None:  # ← УБЕРИ ВСЕ @patch!
        """Тест: успешное чтение CSV."""
        result = read_csv_transactions("transactions.csv")  # ← ТВОЙ ФАЙЛ!
        assert len(result) >= 1

    def test_excel_success(self) -> None:  # ← УБЕРИ ВСЕ @patch!
        """Тест: успешное чтение Excel."""
        result = read_excel_transactions("transactions_excel.xlsx")  # ← ТВОЙ ФАЙЛ!
        assert len(result) >= 1  # ← Много транзакций!

    @patch('pandas.read_excel')
    def test_excel_fail(self, mock_excel: MagicMock) -> None:
        """Тест: ошибка чтения Excel."""
        mock_excel.side_effect = Exception
        result: list[dict[str, Any]] = read_excel_transactions("fail.xlsx")
        assert len(result) == 0
