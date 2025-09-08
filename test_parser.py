import os
import sys
from dsb_parser import DSBLexer, DSBParser


def run_test(input_file, output_dir):
    lexer = DSBLexer()
    parser = DSBParser()

    output_file = os.path.join(
        output_dir, os.path.basename(input_file).replace(".s", "-parser.out")
    )

    with open(input_file, "r") as f:
        code = f.read()

    program = parser.parse(lexer.tokenize(code))

    # program is now a list of Instruction objects
    with open(output_file, "w") as f:
        for instr in program:
            f.write(str(instr) + "\n")

    print(f"[🆗] {input_file} -> {output_file}")


if __name__ == "__main__":
    test_dir = os.path.join(os.path.dirname(__file__), "tests")
    out_dir = os.path.join(os.path.dirname(__file__), "tests/parser_results")

    os.makedirs(out_dir, exist_ok=True)

    # todos os arquivos .s em /tests
    test_files = [f for f in os.listdir(test_dir) if f.endswith(".s")]

    if not test_files:
        print("Nenhum arquivo .s encontrado em /tests")
        sys.exit(1)

    for fname in test_files:
        run_test(os.path.join(test_dir, fname), output_dir=out_dir)
    print("\n[🚀] Todos os testes concluídos.")
