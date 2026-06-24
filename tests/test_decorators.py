import pytest

from src.bankapp.decorators import log


def test_log_decorator_success(capsys):
    """Тест успешного выполнения с print."""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert "Выполняется add" in captured.out
    assert "add завершена успешно" in captured.out


def test_log_decorator_file(tmp_path):
    """Тест записи в файл."""
    log_file = tmp_path / "test.log"

    @log(str(log_file))
    def multiply(x: int) -> int:
        return x * 2

    result = multiply(5)
    assert result == 10

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Выполняется multiply" in content
        assert "multiply завершена успешно" in content


def test_log_decorator_exception(capsys):
    """Тест обработки исключения."""

    @log()
    def divide_zero(x: int) -> float:
        return x / 0

    with pytest.raises(ZeroDivisionError):
        divide_zero(10)

    captured = capsys.readouterr()
    assert "divide_zero вызвала ошибку ZeroDivisionError" in captured.out
