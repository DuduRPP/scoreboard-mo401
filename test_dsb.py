import os
import sys
from dsb import CPU, Scoreboard, load_fu_config
from dsb_parser import DSBLexer, DSBParser


def run_scoreboard(config_file, source_file, out_dir):
    # load FU config
    funits = load_fu_config(config_file)
    scoreboard = Scoreboard()
    cpu = CPU(funits, scoreboard=scoreboard)

    # parse assembly
    lexer = DSBLexer()
    parser = DSBParser()
    with open(source_file) as f:
        instructions = parser.parse(lexer.tokenize(f.read()))
    cpu.load_instructions(instructions)

    # run simulation
    cpu.run()

    # results filename
    base_config = os.path.splitext(os.path.basename(config_file))[0]
    base_source = os.path.splitext(os.path.basename(source_file))[0]
    out_file = os.path.join(out_dir, f"{base_config}-{base_source}.out")

    # dump scoreboard
    with open(out_file, "w") as f:
        f.write(scoreboard.to_markdown())
        f.write("\n")

    print(f"[🆗] {config_file} + {source_file} -> {out_file}")


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    config_dir = os.path.join(base_dir, "tests")
    source_dir = os.path.join(base_dir, "tests")
    results_dir = os.path.join(base_dir, "tests", "results")

    os.makedirs(results_dir, exist_ok=True)

    configs = [f for f in os.listdir(config_dir) if f.endswith(".in")]
    sources = [f for f in os.listdir(source_dir) if f.endswith(".s")]

    if not configs or not sources:
        print("No config (.in) or source (.s) files found.")
        sys.exit(1)

    for cfg in configs:
        for src in sources:
            run_scoreboard(
                os.path.join(config_dir, cfg),
                os.path.join(source_dir, src),
                results_dir,
            )

    print(f"\n[🚀] All scoreboard tests completed. Results in {results_dir}")
