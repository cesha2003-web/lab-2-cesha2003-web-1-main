import inspect

import pytest


@pytest.fixture
def calculate_green_index():
    # Проверяем импорт функции через try-except
    try:
        from task import calculate_green_index as calculate_green_index_
    except ImportError:
        assert False, "Не удалось импортировать функцию `calculate_green_index` из модуля `task`"
    except Exception:
        assert False, f"Неожиданная ошибка в решении :( Запустите ваше решение, чтобы проверить его работоспособность."

    # Проверяем, что импортированная переменная - функция с помощью inspect
    assert inspect.isfunction(calculate_green_index_), "Переменная calculate_green_index не является функцией"

    # Проверяем сигнатуру функции
    sig = inspect.signature(calculate_green_index_)
    params = list(sig.parameters.values())

    assert params, f"Функция должна принимать аргументы"

    # Подсчитываем количество позиционных аргументов (без *args и **kwargs)
    positional_params = [
        p for p in params
        if p.default == inspect.Parameter.empty
    ]

    # Должен быть ровно один позиционный аргумент
    assert len(
        positional_params) == 1, f"Функция должна принимать ровно один позиционный аргумент, но принимает {len(positional_params)}"

    # Проверяем, что функция возвращает результат (не None) на простом тестовом случае
    result = calculate_green_index_([])
    assert result is not None, "Функция calculate_green_index должна возвращать результат, а не None"

    return calculate_green_index_


def test_define_function(calculate_green_index):
    pass


def rich_assert(msg: str, expected, testing_func, *args, **kwargs):
    actual = testing_func(*args, **kwargs)
    args_repr = ', '.join(repr(arg) for arg in args)
    kwargs_repr = ', '.join(f'{key}={repr(value)}' for key, value in kwargs.items())

    all_args = []
    if args_repr:
        all_args.append(args_repr)
    if kwargs_repr:
        all_args.append(kwargs_repr)

    combined_args = ', '.join(all_args)

    assert actual == expected, (
        f"{msg}\n"
        f"assert {testing_func.__name__}({combined_args}) == {expected!r}\n"
        f"Ожидалось: {expected}\n"
        f"Получено: {actual}"
    )


def test_function_annotations_and_docsting(calculate_green_index):
    assert_type_hints(calculate_green_index)
    assert_docstring(calculate_green_index)


def assert_type_hints(func):
    # Получаем сигнатуру функции
    sig = inspect.signature(func)
    params = sig.parameters

    # Проверяем, что у всех параметров есть аннотации типов
    for param_name, param in params.items():
        assert param.annotation != inspect.Parameter.empty, \
            f"Параметр '{param_name}' функции {func.__name__} не имеет аннотации типа"

    # Проверяем, что у возвращаемого значения есть аннотация типа
    assert sig.return_annotation != inspect.Signature.empty, \
        f"Функция {func.__name__} не имеет аннотации типа возвращаемого значения"


def assert_docstring(func):
    # Проверяем, что у функции есть docstring
    assert func.__doc__ is not None and func.__doc__.strip(), \
        f"Функция {func.__name__} не имеет docstring"


def test_realistic_data(calculate_green_index):
    """
    Тест на реалистичных данных с учётом обработки значений None,
    округления до трёх знаков и корректности расчёта индекса озеленения.
    """
    data = [
        {
            "territory_name": "Пушкин",
            "territory_area": 89.24,
            "green_zones": [15.7344, 9.44, None, 2.49]
        },
        {
            "territory_name": "Павловск",
            "territory_area": 36.8,
            "green_zones": [3.82, 2.865, 1.91]
        },
        {
            "territory_name": "Петергоф",
            "territory_area": 48.3,
            "green_zones": [4.5, 9, 2.25]
        }
    ]

    expected_result = {
        "Пушкин": 0.31,
        "Павловск": 0.234,
        "Петергоф": 0.326
    }

    rich_assert(
        "Ошибка в расчёте индекса озеленения.",
        expected_result,
        calculate_green_index,
        data
    )


def test_handling_none_values(calculate_green_index):
    """
    Тест на обработку значений None в списке green_zones.
    """
    data = [
        {
            "territory_name": "Территория 1",
            "territory_area": 100,
            "green_zones": [10, None, 20]
        },
        {
            "territory_name": "Территория 2",
            "territory_area": 200,
            "green_zones": [None, None, 50]
        }
    ]
    expected_result = {
        "Территория 1": 0.300,
        "Территория 2": 0.250
    }
    rich_assert(
        "Ошибка при обработке значений None. Убедитесь, что значения None игнорируются.",
        expected_result,
        calculate_green_index,
        data
    )


def test_empty_green_zones(calculate_green_index):
    """
    Тест на пустой список зелёных зон.
    """
    data = [
        {
            "territory_name": "Территория 1",
            "territory_area": 500,
            "green_zones": []
        },
        {
            "territory_name": "Территория 2",
            "territory_area": 1000,
            "green_zones": []
        }
    ]
    expected_result = {
        "Территория 1": 0.000,
        "Территория 2": 0.000
    }
    rich_assert(
        "Ошибка при пустом списке зелёных зон. Индекс озеленения должен быть равен 0.",
        expected_result,
        calculate_green_index,
        data
    )


def test_all_none_in_green_zones(calculate_green_index):
    """
    Тест на все значения None в списке green_zones.
    """
    data = [
        {
            "territory_name": "Территория 1",
            "territory_area": 500,
            "green_zones": [None, None, None]
        }
    ]
    expected_result = {
        "Территория 1": 0,
    }
    rich_assert(
        "Ошибка при всех значениях None в зелёных зонах. Индекс озеленения должен быть равен 0.",
        expected_result,
        calculate_green_index,
        data
    )


def test_rounding_no_change(calculate_green_index):
    """
    Тест на округление до трёх знаков после запятой.
    Число остаётся без изменений (меньше трёх знаков).
    """
    data = [
        {
            "territory_name": "Территория 1",
            "territory_area": 10000,
            "green_zones": [1200]
        }
    ]
    expected_result = {
        "Территория 1": 0.12,
    }
    rich_assert(
        "Ошибка при округлении. Число должно остаться без изменений (меньше трёх знаков после запятой).",
        expected_result,
        calculate_green_index,
        data
    )


def test_rounding_down(calculate_green_index):
    """
    Тест на округление до трёх знаков после запятой.
    Округление в меньшую сторону.
    """
    data = [
        {
            "territory_name": "Территория 2",
            "territory_area": 10000,
            "green_zones": [1234]
        }
    ]
    expected_result = {
        "Территория 2": 0.123,
    }
    rich_assert(
        "Ошибка при округлении в меньшую сторону.",
        expected_result,
        calculate_green_index,
        data
    )


def test_rounding_up(calculate_green_index):
    """
    Тест на округление до трёх знаков после запятой.
    Округление в большую сторону.
    """
    data = [
        {
            "territory_name": "Территория 3",
            "territory_area": 10000,
            "green_zones": [1237]
        }
    ]
    expected_result = {
        "Территория 3": 0.124,
    }
    rich_assert(
        "Ошибка при округлении в большую сторону.",
        expected_result,
        calculate_green_index,
        data
    )


def test_empty_input_list(calculate_green_index):
    """
    Тест на пустой входной список.
    """
    data = []
    expected_result = {}
    rich_assert(
        "Ошибка при пустом входном списке. Функция должна возвращать пустой словарь.",
        expected_result,
        calculate_green_index,
        data
    )
