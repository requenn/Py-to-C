TOKEN_ID = "Id"
TOKEN_INT = "Int"
TOKEN_FLOAT = "Float"
TOKEN_ASSIGN = "Assign"
TOKEN_END = "End"


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __str__(self):
        if self.value is not None:
            return f"{self.type} {self.value}"
        return self.type


class Lexer:
    def __init__(self, filename):
        self.file = open(filename, "r", encoding="utf-8")
        self.ch = self.file.read(1)

    def advance(self):
        self.ch = self.file.read(1)

    def skip_whitespace(self):
        while self.ch != "" and self.ch.isspace():
            self.advance()

    def read_identifier(self):
        name = ""
        while self.ch != "" and (self.ch.isalnum() or self.ch == "_"):
            name += self.ch
            self.advance()
        return Token(TOKEN_ID, name)

    def read_number(self):
        num = ""
        is_float = False

        if self.ch == "-":
            num += self.ch
            self.advance()

        while self.ch != "" and self.ch.isdigit():
            num += self.ch
            self.advance()

        if self.ch == ".":
            is_float = True
            num += self.ch
            self.advance()
            while self.ch != "" and self.ch.isdigit():
                num += self.ch
                self.advance()

        if is_float:
            return Token(TOKEN_FLOAT, num)
        return Token(TOKEN_INT, num)

    def get_token(self):
        self.skip_whitespace()

        if self.ch == "":
            return Token(TOKEN_END)

        if self.ch.isalpha() or self.ch == "_":
            return self.read_identifier()

        if self.ch.isdigit() or self.ch == "-":
            return self.read_number()

        if self.ch == "=":
            self.advance()
            return Token(TOKEN_ASSIGN)

        unknown = self.ch
        self.advance()
        raise SyntaxError(f"Неизвестный символ: '{unknown}'")

    def close(self):
        self.file.close()