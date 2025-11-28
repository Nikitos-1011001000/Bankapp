import pytest

from bankapp.processing import filter_by_state
from bankapp.processing import sort_by_date


@pytest.fixture(params=[
    # (входной список словарей, параметр state, ожидаемый результат)
    (
        [{'state': 'active'}, {'state': 'inactive'}, {'state': 'active'}],
        'active',
        [{'state': 'active'}, {'state': 'active'}]
    ),
    (
        [{'state': 'active'}, {'state': 'inactive'}],
        'inactive',
        [{'state': 'inactive'}]
    ),
    (
        [{'state': 'active'}, {'state': 'inactive'}],
        'pending',  # состояния 'pending' нет в списке
        []
    ),
    (
        [],  # пустой список
        'active',
        []
    ),
    (
        [{'state': None}, {'state': 'active'}],
        None,
        [{'state': None}]
    )
])
def filter_test_data(request):
    return request.param


def test_filter_by_state(filter_test_data):
    items, state, expected = filter_test_data
    assert filter_by_state(items, state) == expected

    @pytest.fixture(params=[
        # Сортировка по возрастанию с разными датами
        (
            [
                    {'date': '2024-01-02'},
                    {'date': '2023-12-31'},
                    {'date': '2024-01-01'}
                    ],
            True,
            [
                {'date': '2023-12-31'},
                {'date': '2024-01-01'},
                {'date': '2024-01-02'}
            ]
        ),
        # Сортировка по убыванию с одинаковыми датами
        (
            [
                {'date': '2024-01-01'},
                {'date': '2024-01-01'},
                {'date': '2023-12-30'}
            ],
            False,
            [
                {'date': '2024-01-01'},
                {'date': '2024-01-01'},
                {'date': '2023-12-30'}
            ]
        ),
        # Нестандартный формат, дата отсутствует, должна идти первой (минимум)
        (
            [
                {'date': 'invalid-date'},
                {'date': '2024-01-01'},
                {'date': None}
            ],
            True,
            [
                {'date': 'invalid-date'},
                {'date': None},
                {'date': '2024-01-01'}
            ]
        ),
        # Пустой входной список
        (
            [],
            True,
            []
        )
    ])
    def sort_data(request):
        return request.param

    def test_sort_by_date(sort_data):
        items, ascending, expected = sort_data
        result = sort_by_date(items, ascending=ascending)
        assert result == expected
