"""
AST Nodes:

program = Program(function_definition)
function_definition = Function(identifier name, statement body)
statement = Return(exp)
exp = Constant(int) | Unary(unary_operator, exp)
unary_operator = Complement | Negate

"""

class ASTNode:
    pass

class Exp(ASTNode):
    pass

class UnaryOperator:
    pass

class Complement(UnaryOperator):
    pass

class Negate(UnaryOperator):
    pass

class Constant(Exp):
    def __init__(self, value: int):
        self.value = value

class Unary(Exp):
    def __init__(self, unary_operator: UnaryOperator, exp: Exp):
        self.unary_operator = unary_operator
        self.exp = exp

class Statement(ASTNode):
    pass

class ReturnStatement(Statement):
    def __init__(self, return_value: Exp):
        self.return_value = return_value

class Identifier(ASTNode):
    def __init__(self, name_str: str):
        self.name_str = name_str

class FunctionDefinition(ASTNode):
    def __init__(self, name: Identifier, body: Statement):
        self.name = name
        self.body = body

class Program(ASTNode):
    def __init__(self, function_definition: FunctionDefinition):
        self.function_definition = function_definition

"""
Formal Grammar:

<program> ::= <function>
<function> ::= "int" <identifier> "(" "void" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <int> | <unop> <exp> | "(" <exp> ")"
<unop> ::= "-" | "~"
<identifier> ::= ? An identifier token ?
<int> ::= ? A constant token ?

"""

# Recursive Descent Parsing

from lexer import *

def take_token(tokens):
    print(f"took {tokens[0].token_type}, {tokens[0].string}")
    try:
        x = tokens[0]
        del tokens[0]
        return x
    except IndexError as e:
        raise Exception("Invalid end of program!") from e

def expect(expected: TokenType, tokens):
    print(f"expected {expected}")
    actual = take_token(tokens).token_type
    if actual != expected:
        raise Exception(f"Expected {expected} but found {actual}!")

def parse_identifier(tokens):
    # check if identifier
    try:
        if tokens[0].token_type != TokenType.identifier:
            raise Exception(f"Invalid identifier: {tokens[0].string}!")
    except IndexError as e:
        raise Exception("Invalid end of program!")
    identifier = take_token(tokens).string
    return Identifier(identifier)

def parse_int(tokens):
    # check if int
    try:
        if tokens[0].token_type != TokenType.constant:
            raise Exception(f"Invalid constant: {tokens[0].string}!")
    except IndexError as e:
        raise Exception("Invalid end of program!")
    int = take_token(tokens).string
    return Constant(int)

def parse_unary(tokens):
    match tokens[0].token_type:
        case TokenType.hyphen:
            take_token(tokens)
            return Unary(Negate(), parse_exp(tokens))
        case TokenType.tilde:
            take_token(tokens)
            return Unary(Complement(), parse_exp(tokens))

def parse_parenthesized_exp(tokens):
    take_token(tokens)
    inner_exp = parse_exp(tokens)
    expect(TokenType.close_parenthesis, tokens)
    return inner_exp

def parse_exp(tokens):
    val = None
    match tokens[0].token_type:
        case TokenType.constant:
            val = parse_int(tokens)
        case TokenType.tilde | TokenType.hyphen:
            val = parse_unary(tokens)
        case TokenType.open_parenthesis:
            val = parse_parenthesized_exp(tokens)
        case _:
            raise Exception('No expression found!')
    return val

def parse_statement(tokens):
    expect(TokenType.return_keyword, tokens)
    return_val = parse_exp(tokens)
    expect(TokenType.semicolon, tokens)
    return ReturnStatement(return_value=return_val)

def parse_function(tokens):
    expect(TokenType.int_keyword, tokens)
    identifier = parse_identifier(tokens)
    expect(TokenType.open_parenthesis, tokens)
    expect(TokenType.void_keyword, tokens)
    expect(TokenType.close_parenthesis, tokens)
    expect(TokenType.open_brace, tokens)
    statement = parse_statement(tokens)
    expect(TokenType.close_brace, tokens)
    return FunctionDefinition(identifier, statement)

def parse_program(tokens):
    function = parse_function(tokens)
    if len(tokens) != 0:
        raise Exception("Invalid end of program!")
    return Program(function)

def print_program(program: Program, indent: int = 0):
    def print_indent(text):
        print(" " * indent + text)

    print_indent("Program:")
    indent += 2

    function_def = program.function_definition

    print_indent(f"FunctionDefinition: {function_def.name.name_str}")
    indent += 2

    body = function_def.body

    print_indent("ReturnStatement:")
    indent += 2
    return_value = body.return_value
    if isinstance(return_value, Constant):
        print_indent(f"Constant: {return_value.value}")
    elif isinstance(return_value, Identifier):
        print_indent(f"Identifier: {return_value.name_str}")
    else:
        print_indent("Unknown return value.")
    indent -= 2

    indent -= 4

# x = """
# int main(void) {
#     return ~-2147483647;
# }
# """

# t = tokenize(x)

# for i in t:
#     print(f"'{i.string}' {i.token_type}")

# p = parse_program(t)

# print_program(p)
