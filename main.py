#!/usr/bin/env python3
"""Анализатор банковских транзакций."""
import csv
import logging
from typing import Any, Dict, List, Optional
from src.bankapp.processing import process_bank_search, sort_by_date
from src.bankapp.utils import load_transactions
from src.bankapp.widget import get_date, mask_account_card


def load_csv(path: str) -> List[Dict[str, Any]]:
    """Загрузка CSV в JSON формат."""
    data: List[Dict[str, Any]] = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                operation = {
                    "id": row.get("id", ""),
                    "state": row.get("state", ""),
                    "date": row.get("date", ""),
                    "operationAmount": {
                        "amount": row.get("amount", "0"),  # ✅ amount!
                        "currency": {
                            "name": row.get("currency_name", "руб."),
                            "code": row.get("currency_code", "810")  # ✅ currency_code!
                        }
                    },
                    "description": row.get("description", ""),
                    "from": row.get("from", ""),
                    "to": row.get("to", "")
                }
                data.append(operation)
        # print(f"=== CSV DEBUG: Загружено {len(data)} операций ===") #
        return data
    except Exception as e:
        logging.error(f"Ошибка CSV {path}: {e}")
        return []


def load_xlsx(path: str) -> List[Dict[str, Any]]:
    """Загрузка XLSX."""
    try:
        df = pd.read_excel(path, engine='openpyxl')
        data = df.to_dict('records')

        normalized = []
        for row in data:
            operation = {
                "id": str(row.get("id", "")),
                "state": row.get("state", ""),
                "date": row.get("date", ""),
                "operationAmount": {  # ✅ НОРМАЛИЗАЦИЯ!
                    "amount": str(row.get("amount", "0")),
                    "currency": {
                        "name": row.get("currency_name", "Ruble"),
                        "code": row.get("currency_code", "RUB")  # ✅ RUB!
                    }
                },
                "description": row.get("description", ""),
                "from": row.get("from", ""),
                "to": row.get("to", "")
            }
            normalized.append(operation)
        return normalized
    except Exception as e:
        logging.error(f"Ошибка XLSX {path}: {e}")
        return []


def get_status_menu() -> str:
    """Меню статусов."""
    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print(f"Доступные для фильтровки статусы: {', '.join(statuses)}")

    while True:
        user_input = input().strip().upper()
        if user_input in statuses:
            return user_input
        print(f'Статус операции "{user_input}" недоступен.')


def get_date_sorting(filtered: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Сортировка по дате."""
    sort_choice = input("Отсортировать операции по дате? Да/Нет: ").lower()

    if sort_choice in ['да', 'yes', 'y', 'д']:
        direction = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        descending = "убыванию" in direction  # ← ИЗМЕНИЛ ТУТ!
        print(f"Операции отсортированы {'по убыванию' if descending else 'по возрастанию'}")
        return sort_by_date(filtered, descending)
    return filtered


def get_rub_filter(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтр рублевых транзакций."""
    rub_choice = input("Выводить только рублевые транзакции? Да/Нет: ").lower()

    if rub_choice in ['да', 'yes', 'y', 'д']:
        rub_transactions: List[Dict[str, Any]] = []
        for tx in transactions:
            operation_amount = tx.get('operationAmount', {})
            currency = operation_amount.get('currency', {})
            code = currency.get('code', '')
            if code in ['RUB', '810']:
                rub_transactions.append(tx)
        print("Показаны только рублевые транзакции")
        return rub_transactions
    return transactions


def get_search_filter(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Поиск по описанию."""
    search_choice = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").lower()

    if search_choice in ['да', 'yes', 'y', 'д']:
        search_term = input("Введите слово для поиска: ")
        result = process_bank_search(transactions, search_term)  # type: ignore
        print(f"Найдено {len(result)} операций с '{search_term}'")
        return result
    return transactions


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Красивый вывод транзакций."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(transactions)}")
    print()

    for tx in transactions[:5]:  # Первые 5
        date = get_date(tx.get('date', ''))  # type: ignore
        desc = tx.get('description', '')
        from_info = tx.get('from', '')
        to_info = tx.get('to', '')
        from_to = f"{mask_account_card(from_info)} -> {mask_account_card(to_info)}"
        amount_info = tx.get('operationAmount', {})
        amount = amount_info.get('amount', '0')
        currency = amount_info.get('currency', {}).get('code', 'RUB')

        print(f"{date} {desc}")
        print(f"{from_to}")
        print(f"Сумма: {amount} {currency}")
        print()


def main() -> None:
    """Главная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Введите номер пункта (1-3): ").strip()

    # 1️⃣ Загрузка данных
    transactions: List[Dict[str, Any]] = []
    if choice == "1":
        json_path = "data/operations.json"
        print(f"Для обработки выбран JSON-файл: {json_path}")
        transactions = load_transactions()
    elif choice == "2":
        csv_path = "transactions.csv"
        print(f"Для обработки выбран CSV-файл: {csv_path}")
        transactions = load_csv(csv_path)
    elif choice == "3":
        xlsx_path = "transactions_excel.xlsx"
        print(f"Для обработки выбран XLSX-файл: {xlsx_path}")
        transactions = load_xlsx(xlsx_path)
    else:
        print("Неверный выбор!")
        return

    if not transactions:
        print("Не удалось загрузить данные из файла. Завершение работы.")
        return

    # 2️⃣ Фильтр по статусу
    status = get_status_menu()
    filtered: List[Dict[str, Any]] = [
        tx for tx in transactions if str(tx.get('state', '')).strip().upper() == status.upper()
    ]
    print(f'Операции отфильтрованы по статусу "{status}" ({len(filtered)} найдено)')

    # 3️⃣ Пошаговая фильтрация
    result = get_date_sorting(filtered)
    result = get_rub_filter(result)
    result = get_search_filter(result)

    # 4️⃣ Вывод результатов
    print_transactions(result)


if __name__ == "__main__":
    main()
