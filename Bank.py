from Parser import Parser


class Bank:
    _parser: Parser
    _name: str

    def __init__(self, name):
        self._name = name
        self._parser = None

    def get_parser(self) -> Parser:
        if self._parser is None:
            raise AttributeError("Parser has not been initialized. Please call set_parser before calling get_parser.")
        return self._parser

    def set_parser(self, parser:Parser):
        self._parser = parser

    def get_name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return ""

    def __repr__(self):
        return f"<Bank name={self.get_name()}>"
