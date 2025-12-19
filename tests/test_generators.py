from bankapp.generators import filter_by_currency
from bankapp.generators import card_number_generator
from bankapp.generators import transaction_descriptions


# Тесты для filter_by_currency
def test_filter_by_currency():

    transactions = [
        {'currency': 'USD', 'amount': 100},
        {'currency': 'EUR', 'amount': 150},
        {'currency': 'USD', 'amount': 50}
    ]
    result = list(filter_by_currency(transactions, 'USD'))
    assert len(result) == 2
    assert all(tx['currency'] == 'USD' for tx in result)


def test_filter_by_currency_no_match():
    transactions = [{'currency': 'GBP', 'amount': 200}]
    result = list(filter_by_currency(transactions, 'USD'))
    assert result == []


def test_filter_by_currency_empty():
    assert list(filter_by_currency([], 'USD')) == []


# Тесты для card_number_generator
def test_card_number_generator_small_range():
    gen = card_number_generator("0000 0000 0000 0001", "0000 0000 0000 0003")
    result = list(gen)
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"

    ]
    assert result == expected


def test_card_number_generator_format():
    gen = card_number_generator("0000 0000 0000 9998", "0000 0000 0000 9999")
    for card in gen:
        assert len(card) == 19  # 16 digits + 3 spaces
        assert card[4] == ' '
        assert card[9] == ' '
        assert card[14] == ' '


# Тесты для transaction_descriptions
def test_transaction_descriptions_basic():
    transactions = [
        {'id': 1, 'amount': 100, 'currency': 'USD'},
        {'id': 2, 'amount': 50, 'currency': 'EUR'}
    ]
    gen = transaction_descriptions(transactions)
    descriptions = list(gen)
    assert descriptions == [
        "Транзакция 1: 100 USD",
        "Транзакция 2: 50 EUR"

    ]


def test_transaction_descriptions_missing_keys():
    transactions = [{'amount': 100}]
    gen = transaction_descriptions(transactions)

    descriptions = list(gen)
    assert descriptions == ["Транзакция N/A: 100 N/A"]


def test_transaction_descriptions_empty():
    assert list(transaction_descriptions([])) == []

    def test_card_number_generator_small_range():
        """Базовый тест: маленький диапазон"""
        gen = card_number_generator(
            "0000 0000 0000 0001",
            "0000 0000 0000 0003",
        )
        result = list(gen)

        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]
        assert result == expected
        assert len(result) == 3

    def test_card_number_generator_format_correct():
        """Тест: правильный формат номеров карт"""
        gen = card_number_generator(
            "0000 0000 0000 9998",
            "0000 0000 0000 9999",
        )
        for card in gen:
            assert len(card) == 19  # 16 цифр + 3 пробела
            assert card[4] == ' '  # после 4 символов
            assert card[9] == ' '  # после 8 символов
            assert card[14] == ' '  # после 12 символов
            assert card.replace(' ', '').isdigit()  # только цифры

    def test_card_number_generator_boundary_values():
        """Тест: граничные значения диапазона"""
        # Начало диапазона
        gen_start = card_number_generator(
            "0000 0000 0000 0001",
            "0000 0000 0000 0001",
        )
        assert next(gen_start) == "0000 0000 0000 0001"

        # Конец диапазона (исключая end+1)
        gen_end = card_number_generator(
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
        )
        result = list(gen_end)
        assert len(result) == 2
        assert result[-1] == "0000 0000 0000 0002"

    def test_card_number_generator_single_value():
        """Тест: диапазон из одного значения"""
        gen = card_number_generator(
            "0000 0000 0000 0001",
            "0000 0000 0000 0001",
        )
        result = list(gen)
        assert len(result) == 1
        assert result[0] == "0000 0000 0000 0001"

    def test_card_number_generator_empty_range():
        """Тест: пустой диапазон (start > end)"""
        gen = card_number_generator(
            "0000 0000 0000 0002",
            "0000 0000 0000 0001",
        )
        result = list(gen)
        assert result == []  # ничего не генерирует

    def test_card_number_generator_generator_exhaustion():
        """Тест: генератор корректно завершается"""
        gen = card_number_generator(
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
        )
        assert next(gen) == "0000 0000 0000 0001"
        assert next(gen) == "0000 0000 0000 0002"

        # Проверяем StopIteration
        try:
            next(gen)
            assert False, "Должен быть StopIteration"
        except StopIteration:
            pass  # ожидаемое поведение

    def test_card_number_generator_large_range():
        """Тест: большой диапазон (не весь, только первые и последние)"""
        gen = card_number_generator(
            "0000 0000 0000 0001",
            "0000 0000 0000 0005",
        )
        result = list(gen)
        assert result[0] == "0000 0000 0000 0001"
        assert result[-1] == "0000 0000 0000 0005"
