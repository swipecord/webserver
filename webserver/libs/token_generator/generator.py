from random import choices
from .chars import symbols


def generate_token(length: int = 32) -> str:
    return "".join(choices(symbols, k=length))
