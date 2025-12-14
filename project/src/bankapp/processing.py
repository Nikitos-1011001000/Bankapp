from datetime import datetime
def filter_by_state(records: list[dict[str, int]], state="EXECUTED"):

    """ Фильтрует список словарей по значению ключа 'state'. """
    return [record for record in records if record.get("state") == state]


def sort_by_date(items, ascending=True):
    def date_key(item):
        return datetime.strptime(item['date'], '%Y-%m-%d')

    return sorted(items, key=date_key, reverse=not ascending)
