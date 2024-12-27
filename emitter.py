from generator import *

def convert_unary_operator(op: UnaryOperator):
    if isinstance(op, Neg):
        return "negl"
    elif isinstance(op, Not):
        return "notl"

def convert_operand(op: Operand):
    if isinstance(op, Imm):
        return f"${str(op.value)}"
    elif isinstance(op, Reg):
        if isinstance(op.reg, AX):
            return f"%eax"
        elif isinstance(op.reg, R10):
            return f"%r10d"
    elif isinstance(op, Stack):
        return f"{op.int}(%rbp)"

def convert_instr(instr: AssemblyInstruction):
    if isinstance(instr, MovAssemblyInstruction):
        src = convert_operand(instr.src)
        dst = convert_operand(instr.dst)
        return f"movl {src}, {dst}"
    elif isinstance(instr, RetAssemblyInstruction):
        return f"movq %rbp, %rsp\n\tpopq %rbp\n\tret"
    elif isinstance(instr, UnaryAssemblyInstruction):
        operator = convert_unary_operator(instr.unary_operator)
        operand = convert_operand(instr.operand)
        return f"{operator} {operand}"
    elif isinstance(instr, AllocateStackAssemblyInstruction):
        return f"subq ${instr.int}, %rsp"

def generate_assembly(program: AssemblyProgram):
    result = ""

    result += f"\t.globl {program.function_definition.name.value}\n"
    result += f"{program.function_definition.name.value}:\n"
    result += f"\tpushq %rbp\n"
    result += f"\tmovq %rsp, %rbp\n"

    for instr in program.function_definition.instructions:
        result += "\t" + convert_instr(instr) + "\n"

    result += f"\t.section .note.GNU-stack,\"\",@progbits\n"

    return result

def write_assembly(program: AssemblyProgram, filename: str):
    text = generate_assembly(program)

    with open(filename, "w") as f:
        f.write(text)

# x = """int main(void) {
#     return ~12;
# }
# """

# t = tokenize(x)
# p = parse_program(t)
# b = tacky_translate(p)
# a = translate(b)
# write_assembly(a, "test.s")
