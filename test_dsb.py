import os
import sys
from dsb import run_simulation


def run_scoreboard(
    config_file, source_file, out_dir, show_hazards=False, hide_scoreboard=False
):
    # Run the simulation (Scoreboard + Hazards list)
    scoreboard, hazards = run_simulation(
        config_file, source_file, detect_hazards=show_hazards
    )

    # Results filename
    base_config = os.path.splitext(os.path.basename(config_file))[0]
    base_source = os.path.splitext(os.path.basename(source_file))[0]
    out_extension = "md"
    out_file = os.path.join(out_dir, f"{base_config}-{base_source}.{out_extension}")

    # Write results
    with open(out_file, "w") as f:
        if show_hazards and hazards:
            f.write("## Hazards detected during execution:\n")
            for hz in dict.fromkeys(hazards):  # deduplicate & preserve order
                f.write(f"- {hz}\n")
            f.write("\n")
            if not hide_scoreboard:
                f.write("## Scoreboard:\n")
        if not hide_scoreboard:
            f.write(scoreboard.to_markdown())
            f.write("\n")

    print(f"[🆗] {config_file} + {source_file} -> {out_file}")


if __name__ == "__main__":
    base_dir = (
        os.path.dirname(os.path.abspath(__file__))
        if "__file__" in globals()
        else os.getcwd()
    )
    config_dir = os.path.join(base_dir, "tests")
    source_dir = os.path.join(base_dir, "tests")

    # Flags
    show_hazards = "-h" in sys.argv
    hide_scoreboard = "--hide-scoreboard" in sys.argv

    results_subdir = "hazards_results" if show_hazards else "results"
    results_dir = os.path.join(base_dir, "tests", results_subdir)
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
                show_hazards=show_hazards,
                hide_scoreboard=hide_scoreboard,
            )

    print(f"\n[🚀] All scoreboard tests completed. Results in {results_dir}")
