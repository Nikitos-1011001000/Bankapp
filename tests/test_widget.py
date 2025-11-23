import pytest
from bankapp.widget import mask_account_card
from bankapp.widget import get_date

@pytest.fixture(params=[
    ("1234567890123456", "1234********3456", False),        # карта 16 цифр
    ("1234 5678 9012 3456", "1234********3456", False),    # карта с пробелами
    ("1234567890123456789", "1234***********6789", False), # карта 19 цифр
    ("1234567890", "1234**7890", False),                    # счет 10 символов
    ("1234567", "1234567", False),                          # короткий счет
    ("AB12CD34EF56GH78", "AB12********GH78", False),       # альфа-цифровая карта
    ("!!!invalid!!!", None, True),                          # некорректный ввод
    ("", "", False),                                        # пустая строка
])
def example_numbers(request):
    return request.param

@pytest.mark.parametrize("input_number, expected_output, expect_error", [
    ("1234", "****", False),
    ("5678", "****", False),
    ("abcd", None, True),
])
def test_mask_account_card(input_number, expected_output, expect_error, request):
    # Если нужны более сложные данные из фикстуры, можно получить их через request.getfixturevalue
    # example_data = request.getfixturevalue("example_numbers")

    if expect_error:
        with pytest.raises(ValueError):
            mask_account_card(input_number)
    else:
        assert mask_account_card(input_number) == expected_output

@pytest.fixture(params=[
            ("2024-12-31", datetime(2024, 12, 31).date()),  # ISO формат
            ("31.12.2024", datetime(2024, 12, 31).date()),  # Европейский формат с точками
            ("12/31/2024", datetime(2024, 12, 31).date()),  # Американский формат с косой чертой
            ("2024/12/31", None),  # Нестандартный формат
            ("", None),  # Пустая строка
            (None, None),  # None вместо строки
            ("random string", None),])
def test_get_date(example_dates):
    input_str, expected_date = example_dates
    assert get_date(input_str) == expected_date

@pytest.fixture(params=[
    ("2024-12-31", datetime(2024, 12, 31).date()),     # ISO формат
    ("31.12.2024", datetime(2024, 12, 31).date()),     # Европейский формат с точками
    ("12/31/2024", datetime(2024, 12, 31).date()),     # Американский формат с косой чертой
    ("2024/12/31", None),                              # Нестандартный формат
    ("", None),                                        # Пустая строка
    (None, None),                                      # None вместо строки
    ("random string", None),                           # Некорректная строка
])
def example_dates(request):
    return request.param

def test_get_date(example_dates):
    input_str, expected_date = example_dates
    assert get_date(input_str) == expected_date