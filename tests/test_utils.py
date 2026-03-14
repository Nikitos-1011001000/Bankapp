import json
import os
import unittest
from typing import Any, Dict, List
from unittest.mock import MagicMock, mock_open, patch

from utils import load_transactions


class TestLoadTransactions(unittest.TestCase):

    def test_file_not_exists(self) -> None:
        """Файл data/operations.json НЕ существует."""
        with patch("utils.os.path.exists") as mock_exists:
            mock_exists.return_value = False

            result: List[Dict[str, Any]] = load_transactions()
            self.assertEqual(result, [])
            mock_exists.assert_called_once_with("data/operations.json")

    def test_valid_json_file(self) -> None:
        """Валидный JSON файл."""
        sample_data: List[Dict[str, Any]] = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]

        with patch("utils.os.path.exists") as mock_exists, patch(
            "builtins.open", new_callable=mock_open, read_data=json.dumps(sample_data)
        ) as mock_file:
            mock_exists.return_value = True
            result: List[Dict[str, Any]] = load_transactions()

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["id"], 1)
            mock_file.assert_called_once_with("data/operations.json", "r", encoding="utf-8")

    def test_empty_json_array(self) -> None:
        """Пустой JSON массив []."""
        with patch("utils.os.path.exists") as mock_exists, patch(
            "builtins.open", new_callable=mock_open, read_data="[]"
        ):
            mock_exists.return_value = True
            result: List[Dict[str, Any]] = load_transactions()
            self.assertEqual(result, [])

    def test_invalid_json_not_list(self) -> None:
        """JSON не список (например, объект {})."""
        invalid_data = {"transactions": []}

        with patch("utils.os.path.exists") as mock_exists, patch(
            "builtins.open", new_callable=mock_open, read_data=json.dumps(invalid_data)
        ):
            mock_exists.return_value = True
            result: List[Dict[str, Any]] = load_transactions()
            self.assertEqual(result, [])

    def test_json_decode_error(self) -> None:
        """Некорректный JSON."""
        with patch("utils.os.path.exists") as mock_exists, patch(
            "builtins.open", new_callable=mock_open, read_data="invalid json {"
        ):
            mock_exists.return_value = True
            result: List[Dict[str, Any]] = load_transactions()
            self.assertEqual(result, [])

    def test_permission_error(self) -> None:
        """PermissionError при открытии файла."""
        with patch("utils.os.path.exists") as mock_exists, patch("builtins.open", side_effect=PermissionError()):
            mock_exists.return_value = True
            result: List[Dict[str, Any]] = load_transactions()
            self.assertEqual(result, [])

    def test_complex_valid_data(self) -> None:
        """Сложные данные — проверяем обработку."""
        complex_data = [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:07.241174",
                "operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}},
            }
        ]

        with patch("utils.os.path.exists") as mock_exists, patch(
            "builtins.open", new_callable=mock_open, read_data=json.dumps(complex_data)
        ):
            mock_exists.return_value = True
            result: List[Dict[str, Any]] = load_transactions()

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["id"], 441945886)
            self.assertEqual(result[0]["state"], "EXECUTED")


if __name__ == "__main__":
    unittest.main()
