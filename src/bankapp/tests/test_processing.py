import pytest

from bankapp.processing import filter_by_state
from bankapp.processing import sort_by_date


@pytest.fixture(
    params=[
        # (входной список словарей, параметр state, ожидаемый результат)
        (
            [{"state": "active"}, {"state": "inactive"}, {"state": "active"}],
            "active",
            [{"state": "active"}, {"state": "active"}],
        ),
        ([{"state": "active"}, {"state": "inactive"}], "inactive", [{"state": "inactive"}]),
        ([{"state": "active"}, {"state": "inactive"}], "pending", []),  # состояния 'pending' нет в списке
        ([], "active", []),  # пустой список
        ([{"state": None}, {"state": "active"}], None, [{"state": None}]),
    ]
)
def filter_test_data(request):
    return request.param


def test_filter_by_state(filter_test_data):
    items, state, expected = filter_test_data
    assert filter_by_state(items, state) == expected


@pytest.fixture(
    params=[
        (
            [{"date": "2024-01-02"}, {"date": "2023-12-31"}, {"date": "2024-01-01"}],
            True,
            [{"date": "2023-12-31"}, {"date": "2024-01-01"}, {"date": "2024-01-02"}],
        ),
        (
            [{"date": "2024-01-01"}, {"date": "2024-01-01"}, {"date": "2023-12-30"}],
            False,
            [{"date": "2024-01-01"}, {"date": "2024-01-01"}, {"date": "2023-12-30"}],
        ),
        (
            [{"date": "invalid-date"}, {"date": "2024-01-01"}, {"date": None}],
            True,
            [{"date": "invalid-date"}, {"date": None}, {"date": "2024-01-01"}],
        ),
        ([], True, []),  # Пустой входной список
    ]
)
def sort_data(request):
    return request.param


def test_sort_by_date():
    sort_data = [{"date": "2024-01-01"}, {"date": "2024-01-01"}, {"date": "2023-12-30"}]

    expected = [{"date": "2023-12-30"}, {"date": "2024-01-01"}, {"date": "2024-01-01"}]
    result = sort_by_date(sort_data)

    assert result == expected
