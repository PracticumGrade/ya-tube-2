from conftest import MAPPING


def reverse(name: str, args: tuple = None) -> str:
    """Функция, которая выполняет преобразование url по имени.
    Так как в задании нет жесткой привязки по name url, сделана эта вспомогательная функция.
    """
    args = args or ()
    return MAPPING[name].format(*args)
