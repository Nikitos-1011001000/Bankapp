import csv
from pathlib import Path
from typing import Any, Dict, List, cast

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает транзакции из CSV файла с обработкой ошибок."""
    transactions: List[Dict[str, Any]] = []
    try:
        path: Path = Path(file_path)
        if not path.exists():
            print(f"❌ Файл не найден: {file_path}")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)  # CSV всегда Dict[str, str]

    except FileNotFoundError:
        print(f"❌ CSV файл не найден: {file_path}")
    except UnicodeDecodeError as e:
        print(f"❌ Ошибка кодировки: {e}")
    except csv.Error as e:
        print(f"❌ Ошибка CSV: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

    return transactions


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает транзакции из Excel файла (.xlsx, .xls) с обработкой ошибок."""
    try:
        path: Path = Path(file_path)
        if not path.exists():
            print(f"❌ Excel файл не найден: {file_path}")
            return []

        df = pd.read_excel(file_path)
        # 🔥 ФИКС: cast решает проблему типов pandas
        return cast(List[Dict[str, Any]], df.to_dict('records'))

    except FileNotFoundError:
        print(f"❌ Excel файл не найден: {file_path}")  # ✅ f-string
    except pd.errors.EmptyDataError:
        print("❌ Пустой Excel файл")
    except ValueError as e:  # ✅ as e
        print(f"❌ Excel ошибка: {e}")
    except Exception as e:  # ✅ as e
        print(f"❌ Неожиданная ошибка Excel: {e}")

    return []