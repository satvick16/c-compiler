#!/usr/bin/env python3

import os
import sys
import subprocess

import lexer
import parser
import tacky
import generator
import emitter

# Parse arguments
OPTIONS = {"--lex", "--parse", "--tacky", "--codegen", "-S"}

input_file = ""
option = ""

for arg in sys.argv[1:]:
    if arg in OPTIONS:
        option = arg
    else:
        input_file = arg

base_name, _ = os.path.splitext(input_file)
preprocessed_file = f"{base_name}.i"
assembly_file = f"{base_name}.s"
output_file = base_name

# Preprocessing
preprocess_cmd = ["gcc", "-E", "-P", input_file, "-o", preprocessed_file]
if subprocess.run(preprocess_cmd).returncode != 0:
    print("Error: Preprocessing failed.", file=sys.stderr)
    sys.exit(1)

# Lexing
try:
    print("Lexing completed (stub)")
    f1 = open(preprocessed_file, "r")
    f1_content = f1.read()
    f1.close()
    tokens = lexer.tokenize(f1_content)
except Exception:
    sys.exit(1)

if option == "--lex":
    if os.path.exists(preprocessed_file):
        os.remove(preprocessed_file)
    sys.exit(0)

# Parsing
try:
    print("Parsing completed (stub)")
    program = parser.parse_program(tokens)
except Exception:
    sys.exit(1)

if option == "--parse":
    if os.path.exists(preprocessed_file):
        os.remove(preprocessed_file)
    sys.exit(0)

# Tacky
try:
    print("Tacky completed (stub)")
    tacky_program = tacky.tacky_translate(program)
except Exception:
    sys.exit(1)

if option == "--tacky":
    if os.path.exists(preprocessed_file):
        os.remove(preprocessed_file)
    sys.exit(0)

# Generation
try:
    print("Code generation completed (stub)")
    assembly_program = generator.translate(tacky_program)
except Exception:
    sys.exit(1)

if option == "--codegen":
    if os.path.exists(preprocessed_file):
        os.remove(preprocessed_file)
    sys.exit(0)

# Emission
try:
    print(f"Assembly file created at {assembly_file}")
    emitter.write_assembly(program=assembly_program, filename=assembly_file)
except Exception:
    sys.exit(1)

if option == "-S":
    if os.path.exists(preprocessed_file):
        os.remove(preprocessed_file)

# Assemble and link
assemble_cmd = ["gcc", assembly_file, "-o", output_file]
if subprocess.run(assemble_cmd).returncode != 0:
    print("Error: Assembly and linking failed.", file=sys.stderr)
    if os.path.exists(assembly_file):
        os.remove(assembly_file)
    sys.exit(1)
if os.path.exists(assembly_file):
    os.remove(assembly_file)

print(f"Executable created at {output_file}")
sys.exit(0)
