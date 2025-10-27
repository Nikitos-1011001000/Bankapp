<<<<<<< HEAD
def filter_by_state(records: list[dict[str, int]], state="EXECUTED"):
=======
def filter_by_state(records: int, state="EXECUTED"):
>>>>>>> 608620d187556f7cabee5311adaf3cc6b8a7513c
    """ Фильтрует список словарей по значению ключа 'state'. """
    return [record for record in records if record.get("state") == state]


<<<<<<< HEAD
def sort_by_date(records: list[dict[str, int]], descending=True):
=======
def sort_by_date(records: int, descending=True):
>>>>>>> 608620d187556f7cabee5311adaf3cc6b8a7513c
    """принимает список словарей и параметр, задающий порядок сортировки возвращает сортировку по дате"""

    return sorted(records, key=lambda x: x.get("date"), reverse=descending)
