def filter_by_currency(transactions, currency):
    return (tx for tx in transactions if tx.get('currency') == currency)


def card_number_generator(start, end):
    # Преобразуем старт и энд в целые числа без пробелов
    start_num = int(start.replace(" ", ""))
    end_num = int(end.replace(" ", ""))

    for num in range(start_num, end_num + 1):
        # Преобразуем число обратно в строку с ведущими нулями до 16 цифр
        num_str = f"{num:016d}"
        # Форматируем строку как 'XXXX XXXX XXXX XXXX'
        formatted = " ".join(num_str[i:i + 4] for i in range(0, 16, 4))
        yield formatted


def transaction_descriptions(transactions):
    for tx in transactions:
        description = f"Транзакция {tx.get('id', 'N/A')}: {tx.get('amount', 0)} {tx.get('currency', 'N/A')}"
        yield description