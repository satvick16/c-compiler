"""
Assembly program:

program = Program(function_definition)
function_definition = Function(identifier name, instruction* instructions)
instruction = Mov(operand src, operand dst) | Ret
operand = Imm(int) | Register

"""

from typing import List

class RegType:
    pass

class AX(RegType):
    pass

class R10(RegType):
    pass

class AssemblyASTNode:
    pass

class Operand(AssemblyASTNode):
    pass

class Imm(Operand):
    def __init__(self, value: int):
        self.value = value

class Reg(Operand):
    def __init__(self, reg: RegType):
        self.reg = reg

class Pseudo(Operand):
    def __init__(self, identifier: str):
        self.identifier = identifier

class Stack(Operand):
    def __init__(self, int: int):
        self.int = int

class AssemblyInstruction(AssemblyASTNode):
    pass

class MovAssemblyInstruction(AssemblyInstruction):
    def __init__(self, src: Operand, dst: Operand):
        self.src = src
        self.dst = dst

class UnaryOperator(AssemblyASTNode):
    pass

class Neg(UnaryOperator):
    pass

class Not(UnaryOperator):
    pass

class UnaryAssemblyInstruction(AssemblyInstruction):
    def __init__(self, unary_operator: UnaryOperator, operand: Operand):
        self.unary_operator = unary_operator
        self.operand = operand

class AllocateStackAssemblyInstruction(AssemblyInstruction):
    def __init__(self, int: int):
        self.int = int

class RetAssemblyInstruction(AssemblyInstruction):
    pass

class AssemblyIdentifier(AssemblyASTNode):
    def __init__(self, value: str):
        self.value = value

class AssemblyFunctionDefinition(AssemblyASTNode):
    def __init__(self, name: AssemblyIdentifier, instructions: List[AssemblyInstruction]):
        self.name = name
        self.instructions = instructions

class AssemblyProgram(AssemblyASTNode):
    def __init__(self, function_definition: AssemblyFunctionDefinition):
        self.function_definition = function_definition

"""
AST node                        Assembly construct
------------------------------------------------------------
Program(function_definition)    Program(function_definition)
Function(name, body)            Function(name, instructions)
Return(exp)                     Mov(exp, Register)
                                Ret
Constant(int)                   Imm(int)

"""

from tacky import *

# def translate(program: Program):
#     return AssemblyProgram(
#         AssemblyFunctionDefinition(
#             AssemblyIdentifier(
#                 program.function_definition.name.name_str
#             ), 
#             [
#                 MovAssemblyInstruction(
#                     Imm(program.function_definition.body.return_value.value),
#                     Register()
#                 ), 
#                 RetAssemblyInstruction()
#             ]
#         )
#     )

def translate(program: TackyProgram):
    instructions = []

    for i in program.function_definition.instructions:
        if isinstance(i, TackyReturn):
            if isinstance(i.val, TackyConstant):
                instructions.append(MovAssemblyInstruction(Imm(i.val.int), Reg(AX())))
            elif isinstance(i.val, TackyVar):
                instructions.append(MovAssemblyInstruction(Pseudo(i.val.identifier.name_str), Reg(AX())))

            instructions.append(RetAssemblyInstruction())
        elif isinstance(i, TackyUnary):
            if isinstance(i.src, TackyConstant):
                src = Imm(i.src.int)
            elif isinstance(i.src, TackyVar):
                src = Pseudo(i.src.identifier.name_str)

            if isinstance(i.dst, TackyConstant):
                dst = Imm(i.dst.int)
            elif isinstance(i.dst, TackyVar):
                dst = Pseudo(i.dst.identifier.name_str)

            instructions.append(MovAssemblyInstruction(src, dst))
            
            if isinstance(i.unary_operator, TackyComplement):
                instructions.append(UnaryAssemblyInstruction(Not()))
            elif isinstance(i.unary_operator, TackyNegate):
                instructions.append(UnaryAssemblyInstruction(Neg()))

    return AssemblyProgram(
        AssemblyFunctionDefinition(
            program.function_definition.identifier.name_str, 
            instructions
        )
    )

# x = """
# int main(void) {
#     return 100;
# }
# """

# t = tokenize(x)
# p = parse_program(t)
# a = translate(p)
