import os
import sys
from dsb_parser import DSBLexer, DSBParser

def run_test(input_file):
    lexer = DSBLexer()
    parser = DSBParser()

    output_file = input_file.replace(".s", "-parser.out")
    results = []

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            instr = parser.parse(lexer.tokenize(line))
            results.append(str(instr))

    with open(output_file, "w") as f:
        for r in results:
            f.write(r + "\n")

    print(f"[🆗] {input_file} -> {output_file}")

if __name__ == "__main__":
    test_dir = os.path.join(os.path.dirname(__file__), "tests")

    # todos os arquivos .s em /tests
    test_files = [f for f in os.listdir(test_dir) if f.endswith(".s")]

    if not test_files:
        print("Nenhum arquivo .s encontrado em /tests")
        sys.exit(1)

    for fname in test_files:
        run_test(os.path.join(test_dir, fname))
    print(f"\n[🚀] Todos os testes concluídos.")
