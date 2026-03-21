from typing import Any
from unittest.mock import MagicMock, Mock, mock_open, patch
from file_parser import read_csv_transactions, read_excel_transactions


class TestFileParser:
    @patch('builtins.open')
    def test_csv_file_not_found(self, mock_open: Mock) -> None:
        """Тест: CSV файл не найден."""
        mock_open.side_effect = FileNotFoundError
        result: list[dict[str, Any]] = read_csv_transactions("missing.csv")
        assert len(result) == 0

    @patch('builtins.open', new_callable=mock_open, read_data="date,amount\ndata")
    def test_csv_success(self, mock_file: mock_open) -> None:
        """Тест: успешное чтение CSV."""
        result: list[dict[str, Any]] = read_csv_transactions("test.csv")
        assert len(result) == 1

    @patch('pandas.read_excel')
    def test_excel_success(self, mock_excel: MagicMock) -> None:
        """Тест: успешное чтение Excel."""
        mock_df: Mock = Mock()
        mock_df.to_dict.return_value = [{'test': 1}]
        mock_excel.return_value = mock_df
        result: list[dict[str, Any]] = read_excel_transactions("test.xlsx")
        assert len(result) == 1

    @patch('pandas.read_excel')
    def test_excel_fail(self, mock_excel: MagicMock) -> None:
        """Тест: ошибка чтения Excel."""
        mock_excel.side_effect = Exception
        result: list[dict[str, Any]] = read_excel_transactions("fail.xlsx")
        assert len(result) == 0
