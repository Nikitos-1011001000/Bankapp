import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала, конца и результата выполнения функции.
    При ошибке — логирует имя функции, параметры и тип исключения.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__
            log_message = f"Выполняется {func_name}\n"

            # Формируем строку с аргументами
            args_str = ", ".join(repr(arg) for arg in args)
            kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            all_args = ", ".join(filter(None, [args_str, kwargs_str]))

            try:
                result = func(*args, **kwargs)
                log_message += f"{func_name} завершена успешно. " f"Результат: {result}\n"

                _write_log(log_message, filename)
                return result
            except Exception as e:
                log_message += f"{func_name} вызвала ошибку {type(e).__name__}: {e}." f"Аргументы: ({all_args})"
                _write_log(log_message, filename)
                raise  # Перебрасываем исключение дальше

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """Вспомогательная функция для записи лога в файл или вывода в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
