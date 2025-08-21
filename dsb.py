import sys
from typing import List, Dict
import pandas as pd

from dsb_parser import Instruction

class CPU:
    def __init__(self, funits, scoreboard):
        self.cycle: int = 0
        self.funits: Dict[str, FunctionalUnit] = funits
        #ADICIONAR LISTA NO PARSER self.instructions: List[Instruction] = []
        self.scoreboard: Scoreboard = scoreboard

    def load_instructions(self, instructions):
        self.instructions = instructions
        for instr in instructions:
            self.scoreboard.add_entry(instr)

    def tick(self):
        self.cycle += 1
        for fu in self.funits.values():
            fu.tick()

class FunctionalUnit:
    def __init__(self, count, cost):
        self.count: int = count
        self.cost: int = cost
        self.instructions: List[Instruction] = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def __len__(self):
        return len(self.instructions)


class Scoreboard:
    def __init__(self):
        self.records = []

    def add_entry(self, instr, issue=None, read=None, execute=None, write=None):
        self.records.append({
            "Instruction": instr,
            "Issue": issue,
            "Read": read,
            "Execute": execute,
            "Write": write,
        })

    def update_entry(self, idx, stage, cycle):
        """Atualiza um estágio (issue/read/execute/write) da instrução"""
        self.records[idx][stage] = cycle

    def to_dataframe(self):
        return pd.DataFrame(self.records)

    def to_markdown(self):
        return self.to_dataframe().to_markdown(index=False)

def load_fu_config(filename):
    fu_units = {}
    with open(filename) as f:
        for line in f:
            name, count, latency = line.strip().split()
            fu_units[name] = FunctionalUnit(int(count), int(latency))
    return fu_units

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python dsb.py <fu_config.txt> <arquivo.s>")
        sys.exit(1)

    fu_config = sys.argv[1]
    source_code = sys.argv[2]

    funits = load_fu_config(fu_config)
    scoreboard = Scoreboard()

    cpu = CPU(funits, scoreboard=scoreboard)
    cpu.load_instructions([])

    scoreboard.add_entry("Início", issue=cpu.cycle, read=cpu.cycle + 1, execute=cpu.cycle + 2, write=cpu.cycle + 3)


    print(scoreboard.to_markdown())