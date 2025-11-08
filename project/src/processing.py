def filter_by_state(records: list[dict[str, int]], state="EXECUTED"):
    """ Фильтрует список словарей по значению ключа 'state'. """
    return [record for record in records if record.get("state") == state]


def sort_by_date(records: list[dict[str, int]], descending=True):
    """принимает список словарей и параметр, задающий порядок сортировки возвращает сортировку по дате"""

    return sorted(records, key=lambda x: x.get("date"), reverse=descending)
