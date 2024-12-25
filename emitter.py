from generator import *

def convert_instr(instr: AssemblyInstruction):
    if isinstance(instr, MovAssemblyInstruction):
        output = f"mov "

        if isinstance(instr.src, Imm):
            output += f"${str(instr.src.value)}, "
        elif isinstance(instr.src, Register):
            output += f"%eax, "

        if isinstance(instr.dst, Imm):
            output += f"${str(instr.dst.value)}\n"
        elif isinstance(instr.dst, Register):
            output += f"%eax\n"

        return output
    elif isinstance(instr, RetAssemblyInstruction):
        return "ret\n"

def generate_assembly(program: AssemblyProgram):
    result = ""

    result += f"\t.globl {program.function_definition.name.value}\n"
    result += f"{program.function_definition.name.value}:\n"

    for instr in program.function_definition.instructions:
        result += "\t" + convert_instr(instr)

    result += f"\t.section .note.GNU-stack,\"\",@progbits\n"

    return result

def write_assembly(program: AssemblyProgram, filename: str):
    text = generate_assembly(program)

    with open(filename, "w") as f:
        f.write(text)

x = """int main(void) {
    return 100;
}
"""

t = tokenize(x)
p = parse_program(t)
a = translate(p)
write_assembly(a, "test.s")
