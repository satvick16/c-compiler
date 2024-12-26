"""
TACKY:

program = Program(function_definition)
function_definition = Function(identifier, instruction* body)
instruction = Return(val) | Unary(unary_operator, val src, val dst)
val = Constant(int) | Var(identifier)
unary_operator = Complement | Negate

"""

from typing import List

class TackyNode:
    pass

class TackyIdentifier(TackyNode):
    def __init__(self, name_str: str):
        self.name_str = name_str

class TackyInstruction(TackyNode):
    pass

class TackyValue(TackyNode):
    pass

class TackyConstant(TackyValue):
    def __init__(self, int: int):
        self.int = int

class TackyVar(TackyValue):
    def __init__(self, identifier: TackyIdentifier):
        self.identifier = identifier

class TackyReturn(TackyInstruction):
    def __init__(self, val: TackyValue):
        self.val = val

class TackyUnaryOperator(TackyNode):
    pass

class TackyComplement(TackyUnaryOperator):
    pass

class TackyNegate(TackyUnaryOperator):
    pass

class TackyUnary(TackyInstruction):
    def __init__(self, unary_operator: TackyUnaryOperator, src: TackyValue, dst: TackyValue):
        self.unary_operator = unary_operator
        self.src = src
        self.dst = dst

class TackyFunctionDefinition(TackyNode):
    def __init__(self, identifier: TackyIdentifier, instructions: List[TackyInstruction]):
        self.identifier = identifier
        self.instructions = instructions

class TackyProgram(TackyNode):
    def __init__(self, function_definition: TackyFunctionDefinition):
        self.function_definition = function_definition

"""
AST                                             TACKY
---------------------------------------------------------------------------------------------
Return(Constant(3))                             Return(Constant(3))
Return(Unary(Complement, Constant(2)))          Unary(Complement, Constant(2), Var("tmp.0"))
                                                Return(Var("tmp.0"))

Return(Unary(Negate,                            Unary(Negate, Constant(8), Var("tmp.0"))
    Unary(Complement,                           Unary(Complement, Var("tmp.0"), Var("tmp.1"))
        Unary(Negate, Constant(8)))))           Unary(Negate, Var("tmp.1"), Var("tmp.2"))
                                                Return(Var("tmp.2"))

"""

from parser import *

curr_tmp_val = -1

def make_temporary():
    global curr_tmp_val
    curr_tmp_val += 1
    return TackyIdentifier(f"tmp.{str(curr_tmp_val)}")

def convert_unop(op: UnaryOperator):
    if isinstance(op, Complement):
        return TackyComplement()
    elif isinstance(op, Negate):
        return TackyNegate()

def emit_tacky(e: Exp, instructions: list):
    if isinstance(e, Constant):
        return TackyConstant(e.value)
    elif isinstance(e, Unary):
        src = emit_tacky(e.exp, instructions)
        dst_name = make_temporary()
        dst = TackyVar(dst_name)
        tacky_op = convert_unop(e.unary_operator)
        instructions.append(TackyUnary(tacky_op, src, dst))
        return dst

def emit_tacky_return(r: ReturnStatement, instructions: List[TackyInstruction]):
    instructions.append(TackyReturn(emit_tacky(r.return_value, instructions)))

def tacky_translate(p: Program):
    instrs = []
    emit_tacky_return(
        p.function_definition.body, 
        instrs
    )

    return TackyProgram(
        TackyFunctionDefinition(
            identifier=TackyIdentifier(p.function_definition.name.name_str), 
            instructions=instrs
        )
    )

# x = """int main(void) {
#     return ~12;
# }
# """

# t = tokenize(x)
# p = parse_program(t)
# a = tacky_translate(p)
# print("hello")
############################
# x = Program(FunctionDefinition(Identifier("main"), ReturnStatement(Unary(Negate,
#  Unary(Complement,
#  Unary(Negate, Constant(8)))))))
# y = tacky_translate(x)

# for i in y.function_definition.instructions:
#     if isinstance(i, TackyUnary):
#         print(i.src, i.dst)
#     else:
#         print(i)
