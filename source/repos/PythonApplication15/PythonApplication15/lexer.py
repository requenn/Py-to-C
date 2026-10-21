TOKEN_ID = "Id"
TOKEN_INT = "Int"
TOKEN_FLOAT = "Float"
TOKEN_BOOL = "Bool"
TOKEN_ASSIGN = "Assign"
TOKEN_PLUS = "Plus"
TOKEN_MINUS = "Minus"
TOKEN_POW = "Pow"
TOKEN_MUL = "Mul"
TOKEN_DIV = "Div"
TOKEN_LPAREN = "LParen"
TOKEN_RPAREN = "RParen"
TOKEN_END = "End"


class Token:
    """Один распознанный токен"""

    def __init__(self, token_type, value=None):
        """Создает токен с указанным типом и значением

        :param token_type: Название типа токена
        :type token_type: str
        :param value: Значение токена
        :type value: str or None
        """
        self.type = token_type
        self.value = value

    def __str__(self):
        """Делает токен для вывода на экран

        :return: Строка с типом и значением
        :rtype: str
        """
        if self.value is not None:
            return f"{self.type} {self.value}"
        return self.type


class Lexer:
    """Посимвольный считыватель файла разбивающий текст на токены"""

    def __init__(self, filename):
        """Открывает файл с кодом и считывает самый первый символ в буфер

        :param filename: Путь к исходному файлу с кодом на Py
        :type filename: str
        """
        self.file = open(filename, "r", encoding="utf-8-sig")
        self.ch = self.file.read(1)

    def advance(self):
        """Читает следующий один символ из файла и сохраняет его в self.ch

        :return: Ничего не возвращает, обновляет поле self.ch
        :rtype: None
        """
        self.ch = self.file.read(1)

    def skip_whitespace(self):
        """Пропускает пробелы, табуляции, переводы строк

        :return: Ничего не возвращает
        :rtype: None
        """
        while self.ch != "" and (self.ch.isspace() or self.ch in (" ", "\t", "\r", "\n", "\xa0")):
            self.advance()

    def read_identifier_or_keyword(self):
        """Считывает слово целиком и проверяет логическое это значение или имя переменной

        :return: TOKEN_BOOL или TOKEN_ID
        :rtype: Token
        """
        name = ""
        while self.ch != "" and (self.ch.isalnum() or self.ch == "_"):
            name += self.ch
            self.advance()

        if name in ("True", "False"):
            return Token(TOKEN_BOOL, name)
        return Token(TOKEN_ID, name)

    def read_number(self):
        """Считывает число

        :return: TOKEN_INT или дробного числа TOKEN_FLOAT
        :rtype: Token
        """
        num = ""
        is_float = False

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
        """Определяет тип текущего символа и возвращает готовый токен

        :return: Очередной токен или TOKEN_END
        :rtype: Token
        :raises SyntaxError: Если встретился незнакомый символ
        """
        self.skip_whitespace()

        # Если файл пуст или достигнут конец файла
        if self.ch == "":
            return Token(TOKEN_END)

        if self.ch.isalpha() or self.ch == "_":
            return self.read_identifier_or_keyword()

        if self.ch.isdigit():
            return self.read_number()

        if self.ch == "=":
            self.advance()
            return Token(TOKEN_ASSIGN)

        if self.ch == "+":
            self.advance()
            return Token(TOKEN_PLUS, "+")

        if self.ch == "-":
            self.advance()
            return Token(TOKEN_MINUS, "-")

        if self.ch == "*":
            self.advance()
            if self.ch == "*":
                self.advance()
                return Token(TOKEN_POW, "**")
            return Token(TOKEN_MUL, "*")

        if self.ch == "/":
            self.advance()
            return Token(TOKEN_DIV, "/")

        if self.ch == "(":
            self.advance()
            return Token(TOKEN_LPAREN, "(")

        if self.ch == ")":
            self.advance()
            return Token(TOKEN_RPAREN, ")")

        # Страховка при чтении конца файла
        if self.ch == "":
            return Token(TOKEN_END)

        unknown = self.ch
        self.advance()
        raise SyntaxError(f"Неизвестный символ: '{unknown}'")

    def close(self):
        """Закрывает ранее открытый файл.

        :return: Ничего не возвращает.
        :rtype: None
        """
        self.file.close()