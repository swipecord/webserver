from random import choices
from .chars import SYMBOLS


def generate_token(length: int = 32) -> str:
    return "".join(choices(SYMBOLS, k=length))