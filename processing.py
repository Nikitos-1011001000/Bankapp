def filter_by_state(records, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param records: список словарей
    :param state: значение для фильтрации по ключу 'state' (по умолчанию 'EXECUTED')
    :return: новый список словарей с нужным значением 'state'
    """
    return [record for record in records if record.get('state') == state]

def sort_by_date(records, descending=True):
    """принимает список словарей и необязательный параметр, задающий порядок сортировки(по умолчанию — убывание). возвращает новый список, отсортированный по дате"""

    return sorted(records, key=lambda x: x.get('date'), reverse=descending)