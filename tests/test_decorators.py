import pytest
import os
from unittest.mock import patch
from bankapp.decorators import log


# Тестовые функции
def test_log_success_console(capsys):
    """Успешное выполнение, вывод в консоль"""

    @log()
    def add(a, b):
        return a + b

    result = add(5, 3)
    assert result == 8

    captured = capsys.readouterr()
    assert "add(5, 3) - НАЧАЛО" in captured.out
    assert "add - УСПЕХ: 8" in captured.out


def test_log_error_console(capsys):
    """Обработка ошибки, вывод в консоль"""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide(10, 0) - НАЧАЛО" in captured.out
    assert "divide - ОШИБКА: ZeroDivisionError" in captured.out
    assert "Traceback" in captured.out


def test_log_success_file(tmp_path):
    """Успешное выполнение, запись в файл"""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    result = multiply(4, 5)
    assert result == 20

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "multiply(4, 5) - НАЧАЛО" in content
        assert "multiply - УСПЕХ: 20" in content


def test_log_error_file(tmp_path):
    """Обработка ошибки, запись в файл"""
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def bad_func():
        raise ValueError("Тестовая ошибка")

    with pytest.raises(ValueError, match="Тестовая ошибка"):
        bad_func()

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "bad_func() - НАЧАЛО" in content
        assert "bad_func - ОШИБКА: ValueError" in content
        assert "Traceback" in content


def test_log_parameters(capsys):
    @log()
    def complex_func(name, age=25, *, city="Москва"):
        return f"{name} из {city}"

    result = complex_func("Иван", age=30, city="СПб")
    assert result == "Иван из СПб"

    captured = capsys.readouterr()
    # Проверяем наличие ключевых частей
    assert "complex_func(" in captured.out
    assert "Иван" in captured.out
    assert "age=30" in captured.out
    assert "city=СПб" in captured.out
    assert "- НАЧАЛО" in captured.out
    assert "- УСПЕХ" in captured.out


def test_log_preserves_metadata():
    """Декоратор сохраняет метаданные функции"""

    @log()
    def test_func(a: int) -> str:
        """Тестовая функция"""
        return str(a)

    assert test_func.__name__ == "test_func"
    assert "Тестовая функция" in test_func.__doc__
    assert test_func.__annotations__ == {"a": int, "return": str}


def test_log_multiple_calls(capsys):
    """Множественные вызовы одной функции"""

    @log()
    def counter(n):
        return n * 2

    counter(1)
    counter(2)

    captured = capsys.readouterr()
    assert captured.out.count("counter(1) - НАЧАЛО") == 1
    assert captured.out.count("counter - УСПЕХ: 2") == 1
    assert captured.out.count("counter(2) - НАЧАЛО") == 1