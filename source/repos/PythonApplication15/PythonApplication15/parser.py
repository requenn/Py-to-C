from lexer import (
    Lexer,
    TOKEN_ID,
    TOKEN_INT,
    TOKEN_FLOAT,
    TOKEN_BOOL,
    TOKEN_ASSIGN,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_MUL,
    TOKEN_DIV,
    TOKEN_POW,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_END,
)


class NumberNode:
    """Узел синтаксического дерева для чисел."""

    def __init__(self, value):
        """Запоминает значение числа.

        :param value: Строковое представление числа.
        :type value: str
        """
        self.value = value

    def __str__(self):
        """Возвращает число строкой.

        :return: Значение числа.
        :rtype: str
        """
        return str(self.value)

    def to_c(self):
        """Генерирует вызов создания объекта в Си.

        :return: Строка вида INT(42) и др.
        :rtype: str
        """
        if "." in str(self.value):
            return f"FLOAT({self.value})"
        return f"INT({self.value})"


class BoolNode:
    """Узел синтаксического дерева для True и False."""

    def __init__(self, value):
        """Запоминает логическое значение

        :param value: Строка 'True' или 'False'.
        :type value: str
        """
        self.value = value

    def __str__(self):
        """Возвращает значение в виде строки

        :return: 'True' или 'False'.
        :rtype: str
        """
        return str(self.value)

    def to_c(self):
        """Генерирует вызов создания логического объекта в C

        :return: 'TRUE()' или 'FALSE()'.
        :rtype: str
        """
        return "TRUE()" if self.value == "True" else "FALSE()"


class VariableNode:
    """Узел дерева для использования переменной в выражении"""

    def __init__(self, name):
        """Запоминает имя переменной

        :param name: Название переменной
        :type name: str
        """
        self.name = name

    def __str__(self):
        """Возвращает имя переменной

        :return: Имя переменной
        :rtype: str
        """
        return self.name

    def to_c(self):
        """Возвращает имя переменной для кода на C

        :return: Имя переменной.
        :rtype: str
        """
        return self.name


class BinOpNode:
    """Узел бинарной операции над двумя операндами (+, -, *, /, **)."""

    def __init__(self, left, op, right):
        """Сохраняет левую часть, знак действия и правую часть.

        :param left: Левый операнд
        :type left: NumberNode, BoolNode, VariableNode, BinOpNode
        :param op: Знак математической операции ('+', '-', '*', '/', '**').
        :type op: str
        :param right: Правый операнд (узел дерева).
        :type right: NumberNode, BoolNode, VariableNode, BinOpNode
        """
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        """Выводит операцию в скобках для наглядности

        :return: Строка вида '(left op right)'.
        :rtype: str
        """
        return f"({self.left} {self.op} {self.right})"

    def to_c(self):
        """Превращает операцию в вызов С библиотеки object.

        :return: Строка вызова(ADD(x, INT(10))'.
        :rtype: str
        """
        op_map = {
            "+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV",
            "**": "POW_OP",
        }
        fn_name = op_map[self.op]
        return f"{fn_name}({self.left.to_c()}, {self.right.to_c()})"


class AssignNode:
    """Узел присваивания значения переменной."""

    def __init__(self, target, value):
        """Сохраняет имя целевой переменной и узел выражения

        :param target: Название переменной, куда сохраняем
        :type target: str
        :param value: Узел выражения, результат которого присваивается
        :type value: NumberNode or BoolNode or VariableNode or BinOpNode
        """
        self.target = target
        self.value = value

    def __str__(self):
        """Выводит присваивание как в py

        :return: Строка вида 'x = выражение'.
        :rtype: str
        """
        return f"{self.target} = {self.value}"

    def to_c(self, declared_vars):
        """Создает строку присваивания на Си с типом object_t*

        :param declared_vars: Множество уже объявленных ранее переменных
        :type declared_vars: set
        :return: Строка на С (object_t* x = INT(5)').
        :rtype: str
        """
        expr_c = self.value.to_c()
        if self.target not in declared_vars:
            declared_vars.add(self.target)
            return f"    object_t* {self.target} = {expr_c};"
        return f"    {self.target} = {expr_c};"


class ProgramNode:
    """Корневой узел синтаксического дерева всей программы."""

    def __init__(self, statements):
        """Запоминает список всех строк программы

        :param statements: Список узлов (AssignNode).
        :type statements: list[AssignNode]
        """
        self.statements = statements

    def __str__(self):
        """Собирает все строки программы в один текст через перенос строки

        :return: Весь исходный код в виде строки.
        :rtype: str
        """
        return "\n".join(str(stmt) for stmt in self.statements)

    def to_c(self):
        """Формирует полноценный файл на С с инклудами и функцией main

        :return: Готовый текст файла программы на С
        :rtype: str
        """
        declared_vars = set()
        c_lines = [stmt.to_c(declared_vars) for stmt in self.statements]
        body = "\n".join(c_lines)

        return (
            '#include <stdio.h>\n'
            '#include "object.h"\n\n'
            'int main(void) {\n'
            f'{body}\n'
            '    return 0;\n'
            '}\n'
        )


class Parser:
    """Синтаксический анализатор методом рекурсивного спуска."""

    def __init__(self, lexer_instance):
        """Инициализирует анализатор и берет у лексера первый токен

        :param lexer_instance: Экземпляр лексера для чтения токенов
        :type lexer_instance: Lexer
        """
        self.lexer = lexer_instance
        self.current_token = None
        self.advance()

    def advance(self):
        """Запрашивает у лексера следующий токен и сохраняет его

        :return: Ничего не возвращает
        :rtype: None
        """
        self.current_token = self.lexer.get_token()

    def match(self, expected_type):
        """Проверяет тип текущего токена, переходит дальше и возвращает прошлый токен

        :param expected_type: Тип токена который мы ожидаем увидеть
        :type expected_type: str
        :return: Токен совпавший с ожидаемым
        :rtype: Token
        :raises SyntaxError: Если текущий токен не совпадает с ожидаемым
        """
        if self.current_token.type == expected_type:
            token = self.current_token
            self.advance()
            return token
        raise SyntaxError(
            f"Синтаксическая ошибка: ожидался '{expected_type}', получен '{self.current_token.type}'"
        )

    def parse_factor(self):
        """Разбирает базовые элементы: число, булевы, переменную или скобки

        :return: Узел дерева соответствующий разобранному элементу
        :rtype: NumberNode or BoolNode or VariableNode or BinOpNode
        :raises SyntaxError: Если встретился неожиданный токен
        """
        token = self.current_token

        if token.type in (TOKEN_INT, TOKEN_FLOAT):
            self.match(token.type)
            return NumberNode(token.value)

        if token.type == TOKEN_BOOL:
            self.match(TOKEN_BOOL)
            return BoolNode(token.value)

        if token.type == TOKEN_ID:
            self.match(TOKEN_ID)
            return VariableNode(token.value)

        if token.type == TOKEN_LPAREN:
            self.match(TOKEN_LPAREN)
            node = self.parse_expression()
            self.match(TOKEN_RPAREN)
            return node

        raise SyntaxError(f"Недопустимое значение: {token}")

    def parse_power(self):
        """Разбирает операцию возведения в степень

        :return: Узел базового элемента или узел операции BinOpNode
        :rtype: NumberNode or BoolNode or VariableNode or BinOpNode
        """
        node = self.parse_factor()

        if self.current_token.type == TOKEN_POW:
            op_token = self.match(TOKEN_POW)
            right_node = self.parse_power()
            return BinOpNode(node, op_token.value, right_node)

        return node

    def parse_term(self):
        """Разбирает цепочки умножения и деления объединяя их слева направо

        :return: Узел операции или единичный узел
        :rtype: NumberNode or BoolNode or VariableNode or BinOpNode
        """
        node = self.parse_power()

        while self.current_token.type in (TOKEN_MUL, TOKEN_DIV):
            op_token = self.match(self.current_token.type)
            node = BinOpNode(node, op_token.value, self.parse_power())

        return node

    def parse_expression(self):
        """Разбирает цепочки сложения и вычитания

        :return: Узел итогового выражения
        :rtype: NumberNode or BoolNode or VariableNode or BinOpNode
        """
        node = self.parse_term()

        while self.current_token.type in (TOKEN_PLUS, TOKEN_MINUS):
            op_token = self.match(self.current_token.type)
            node = BinOpNode(node, op_token.value, self.parse_term())

        return node

    def parse_statement(self):
        """Разбирает одну строку присваивания

        :return: Узел присваивания AssignNode
        :rtype: AssignNode
        """
        var_token = self.match(TOKEN_ID)
        self.match(TOKEN_ASSIGN)
        val_node = self.parse_expression()
        return AssignNode(var_token.value, val_node)

    def parse(self):
        """Разбирает все строки программы до токена конца файла

        :return: Корневой узел ProgramNode хранящий дерево всей программы
        :rtype: ProgramNode
        """
        statements = []
        while self.current_token.type != TOKEN_END:
            statements.append(self.parse_statement())
        return ProgramNode(statements)


class Coordinator:
    """Координатор разбора, вывода структуры AST и генерации файла С"""

    def __init__(self, filename):
        """Запоминает путь к файлу с кодом Py.

        :param filename: Путь к входному файлу
        :type filename: str
        """
        self.filename = filename

    def run(self):
        """Запускает процесс трансляции, печатает дерево и сохраняет файл .c

        :return: Построенное корневое дерево программы
        :rtype: ProgramNode
        """
        lexer = Lexer(self.filename)
        parser = Parser(lexer)
        ast = parser.parse()
        lexer.close()

        print("--- Собранное дерево AST ---")
        for stmt in ast.statements:
            node_type = type(stmt).__name__
            val_type = type(stmt.value).__name__
            print(
                f"Узел: {node_type} - Переменная: {stmt.target} - Значение: {val_type}({stmt.value})"
            )

        print("\n--- Восстановленный код через __str__ ---")
        print(str(ast))

        print("\n--- Сгенерированный код на Си ---")
        c_code = ast.to_c()
        print(c_code)

        with open("output.c", "w", encoding="utf-8") as f:
            f.write(c_code)

        return ast


if __name__ == "__main__":
    coordinator = Coordinator("input.py")
    coordinator.run() # type: ignore