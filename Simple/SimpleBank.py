from Bank import Bank
from Parser import Parser


class SimpleBank(Bank):
    _parser: Parser
    _name: str

    def __init__(self, name, parser):
        self._name = name
        self._parser = parser

    def get_parser(self) -> Parser:
        return self._parser

    def get_name(self) -> str:
        return self._name