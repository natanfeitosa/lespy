import re

def to_snake_case(name):
    """
    Examples:
        >>> to_snake_case('PythonIsTheBest')
        python_is_the_best
        >>> to_snake_case('pythonIsTheBest')
        python_is_the_best
        >>> to_snake_case('python_is_the_best')
        python_is_the_best
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def ansi_style(value: str, *styles: str) -> str:
    codes = {
        "bold": 1,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "magenta": 35,
        "cyan": 36,
    }

    for style in styles:
        value = f"\x1b[{codes[style]}m{value}"

    return f"{value}\x1b[0m"


def unicodify(value) -> str:
    if isinstance(value, bytes):
        value = value.decode("latin-1")
    if not isinstance(value, str):
        value = str(value)
    return value
