from random import choice


class Inspire:
    quotes: list[str]

    def __init__(self, quotes: list[str]):
        self.quotes = quotes

    def quote(self) -> str:
        return choice(self.quotes)
