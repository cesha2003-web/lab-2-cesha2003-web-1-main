"""Файл для решения задачи."""


def calculate_green_index(territories: list[dict]) -> dict[str, float]:
    """Рассчитывает индекс озеленения для списка территорий.

    Индекс озеленения — отношение суммы площадей зелёных зон к общей площади
    территории. Значения None в списке зелёных зон игнорируются.

    Args:
        territories: список словарей с ключами territory_name, territory_area,
            green_zones.

    Returns:
        Словарь {название_территории: индекс_озеленения}, округлённый до трёх
        знаков после запятой.
    """
    result = {}
    for t in territories:
        green_sum = sum(z for z in t["green_zones"] if z is not None)
        result[t["territory_name"]] = round(green_sum / t["territory_area"], 3)
    return result
