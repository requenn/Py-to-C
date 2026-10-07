from lexer import Lexer, TOKEN_ID, TOKEN_INT, TOKEN_FLOAT, TOKEN_ASSIGN, TOKEN_END

class NumberNode:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class VariableNode:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class AssignNode:
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def __str__(self):
        return f"{self.target} = {self.value}"


class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return "\n".join(str(stmt) for stmt in self.statements)


class Parser:
    def __init__(self, lexer_instance):
        self.lexer = lexer_instance
        self.current_token = None
        self.advance()

    def advance(self):
        self.current_token = self.lexer.get_token()

    def match(self, expected_type):
        if self.current_token.type == expected_type:
            token = self.current_token
            self.advance()
            return token

    def parse_statement(self):
        var_token = self.match(TOKEN_ID)
        self.match(TOKEN_ASSIGN)

        if self.current_token.type in (TOKEN_INT, TOKEN_FLOAT):
            num_token = self.match(self.current_token.type)
            val_node = NumberNode(num_token.value)
        elif self.current_token.type == TOKEN_ID:
            id_token = self.match(TOKEN_ID)
            val_node = VariableNode(id_token.value)
        else:
            raise SyntaxError(f"Недопустимое значение: {self.current_token}")

        return AssignNode(var_token.value, val_node)

    def parse(self):
        statements = []
        while self.current_token.type != TOKEN_END:
            statements.append(self.parse_statement())
        return ProgramNode(statements)


class Coordinator:

  def __init__(self, filename):
    self.filename = filename

  def run(self):
    lexer = Lexer(self.filename)
    parser = Parser(lexer)
    ast = parser.parse()
    lexer.close()

    print("Собранное дерево")
    for stmt in ast.statements:
      node_type = type(stmt).__name__
      val_type = type(stmt.value).__name__
      print(
          f"Узел: {node_type} - Переменная: {stmt.target} - Значение:"
          f" {val_type}({stmt.value})"
      )

    print("\nВосстановленный код через __str__")
    print(str(ast))
    return ast


if __name__ == "__main__":
  coordinator = Coordinator("input.py")
  coordinator.run()