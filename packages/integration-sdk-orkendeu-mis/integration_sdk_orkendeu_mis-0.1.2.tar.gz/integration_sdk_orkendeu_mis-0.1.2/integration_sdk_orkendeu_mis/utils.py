import uuid
import time


def generate_trace_id() -> str:
    """
    Генерирует уникальный идентификатор трассировки.
    :return: Уникальный идентификатор трассировки.
    """

    return str(uuid.uuid4())


def timer(func: callable) -> callable:
    """
    Декоратор для измерения времени выполнения функции.
    :param func: Функция, которую нужно обернуть.
    :return: Обернутая функция.
    """

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function {func.__name__} took {end - start:.4f} seconds to execute.")
        return result
    return wrapper
