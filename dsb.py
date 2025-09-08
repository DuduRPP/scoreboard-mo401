import sys
from typing import List, Dict
import pandas as pd

from dsb_parser import Instruction, DSBLexer, DSBParser


class RegisterTable:
    def __init__(self):
        self.registers: Dict[str, str] = {f"x{i}": None for i in range(32)} | {
            f"f{i}": None for i in range(32)
        }


class CPU:
    def __init__(self, funits, scoreboard):
        self.cycle: int = 0
        self.pc: int = 0

        self.register_table: RegisterTable = RegisterTable()
        self.scoreboard: Scoreboard = scoreboard

        self.funits: Dict[str, FunctionalUnit] = funits
        for fu in self.funits.values():
            fu.register_table = self.register_table
            fu.scoreboard = self.scoreboard
            fu.other_fu = self.funits

        self.instructions: List[Instruction] = []

        self.fu_match = {
            "fld": "int",
            "fsd": "int",
            "fmul": "mult",
            "fdiv": "div",
            "fadd": "add",
            "fsub": "add",
        }

    def load_instructions(self, instructions):
        self.instructions = instructions
        for instr in instructions:
            self.scoreboard.add_entry(instr)

    def run(self):
        while self.pc < len(self.instructions) or not self.scoreboard.finished():
            self.tick()

    def tick(self):
        self.cycle += 1

        if self.pc < len(self.instructions):
            self.try_issue()

        for fu in self.funits.values():
            result = None
            if fu.state != "Read" and fu.state != "Issue" and fu.state != "ReadNext":
                result = fu.tick()
            if result is not None:
                self.scoreboard.update_entry(result[0], result[1], self.cycle)

                # if its a write, update other FUs waiting for this result (WAR hazard - cuidado)
                if result[1] == "Write":
                    for other_fu in self.funits.values():
                        if other_fu.busy:
                            if other_fu.qj == fu.name:
                                other_fu.state = "ReadNext"
                                other_fu.qj = None
                                other_fu.rj = True
                            if other_fu.qk == fu.name:
                                other_fu.state = "ReadNext"
                                other_fu.qk = None
                                other_fu.rk = True

        for fu in self.funits.values():
            if fu.state == "Read" or fu.state == "Issue" or fu.state == "ReadNext":
                result = fu.tick()
                if result is not None:
                    self.scoreboard.update_entry(result[0], result[1], self.cycle)

    def find_available_fu(self, op):
        required_fu = self.fu_match[op]
        for name, fu in self.funits.items():
            if name.startswith(required_fu) and fu.available():
                return name
        return None

    def try_issue(self):
        # Check free functional units
        curr_inst = self.instructions[self.pc]
        required_fu = self.find_available_fu(curr_inst.op)

        WAW_hazard = False

        if len(curr_inst.writes) > 0:
            write_register = curr_inst.writes[0].name
            WAW_hazard = self.register_table.registers[write_register] is not None

        if hazard_detection and WAW_hazard:
            hazards.append(
                f"WAW hazard: (instruction: {self.pc + 1}) {curr_inst.original_instr()} cannot write to {write_register} because it is already being written by another instruction."
            )

        if required_fu is None and hazard_detection:
            hazards.append(
                f"Structural hazard: No available functional unit ({self.fu_match[curr_inst.op]}) for instruction {curr_inst.original_instr()} (instruction: {self.pc+1})"
            )

        # Free FU and no WAW hazards
        if required_fu is not None and not WAW_hazard:
            self.funits[required_fu].add_instruction(curr_inst, self.pc)
            self.scoreboard.update_entry(curr_inst, "Issue", self.cycle)
            self.pc += 1


class FunctionalUnit:
    def __init__(self, name, cost):
        self.name: str = name
        self.cost: int = cost

        self.register_table: RegisterTable = None
        self.scoreboard: Scoreboard = None
        self.other_fu: Dict[str, FunctionalUnit] = None
        self.state: str = "Issue"

        self.op_cycle = 0
        self.busy = False

        self.instruction: Instruction = None
        self.instruction_idx = -1

        self.op = None
        self.fi = None
        self.fj = None
        self.fk = None
        self.qj = None
        self.qk = None
        self.rj = False
        self.rk = False

    def add_instruction(self, instruction, idx):
        self.busy = True
        self.instruction = instruction
        self.instruction_idx = idx
        self.op = instruction.op
        if len(instruction.writes) > 0:
            self.fi = instruction.writes[0]
        if len(instruction.reads) > 0:
            self.fj = instruction.reads[0]
            self.qj = self.register_table.registers.get(self.fj.name)
            if self.qj is None:
                self.rj = True
        if len(instruction.reads) > 1:
            self.fk = instruction.reads[1]
            self.qk = self.register_table.registers.get(self.fk.name)
            if self.qk is None:
                self.rk = True

        if self.fi is not None:
            self.register_table.registers[self.fi.name] = self.name

        # print(f"Added instruction {instruction} to FU {self}")
        # print(
        #     f"State after adding: op={self.op}, fi={self.fi}, fj={self.fj}, fk={self.fk}, qj={self.qj}, qk={self.qk}, rj={self.rj}, rk={self.rk}"
        # )

    def available(self):
        return not self.busy

    def tick(self):
        if self.state == "Issue":
            if self.busy:
                self.state = "Read"
                return None
        if self.state == "ReadNext":
            self.state = "Read"
            return None
        if self.state == "Read":
            # Verify RAW hazards
            if (self.rj is True or self.qj is None) and (
                self.rk is True or self.qk is None
            ):
                self.state = "Execute"
                self.op_cycle = 0
                self.rj = False
                self.rk = False
                return (self.instruction, "Read")
            elif hazard_detection:
                if self.rj is False and self.qj is not None:
                    hazards.append(
                        f"RAW hazard: (instruction: {self.instruction_idx + 1}) {self.instruction.original_instr()} cannot read {self.fj.name} because it is being written by another instruction."
                    )
                if self.rk is False and self.qk is not None:
                    hazards.append(
                        f"RAW hazard: (instruction: {self.instruction_idx + 1}) {self.instruction.original_instr()} cannot read {self.fk.name} because it is being written by another instruction."
                    )
        if self.state == "Execute":
            self.op_cycle += 1
            if self.op_cycle >= self.cost:
                self.state = "Write"
                return (self.instruction, "Execute")
        if self.state == "Write":
            # Write result
            if self.fi is not None:
                # TODO: Need to verify WAR hazards, checking if another instruction before is still waiting to read this register
                # If so, do not write and wait for next cycle
                # PROBABLY NEED TO CHANGE WHERE FU TABLE IS STORED (CHANGE TO CPU?)

                for other_fu in self.other_fu.values():
                    if (
                        not other_fu.busy
                        or other_fu.state != "Read"
                        or other_fu is self
                    ):
                        continue
                    # Verify if other_fu is waiting
                    if (
                        other_fu.fj is not None
                        and other_fu.fj.name == self.fi.name
                        and other_fu.instruction_idx < self.instruction_idx
                    ) or (
                        other_fu.fk is not None
                        and other_fu.fk.name == self.fi.name
                        and other_fu.instruction_idx < self.instruction_idx
                    ):
                        if hazard_detection:
                            hazards.append(
                                f"WAR hazard: (instruction: {self.instruction_idx + 1}) {self.instruction.original_instr()} cannot write to {self.fi.name} because {other_fu.instruction.original_instr()} needs to read it."
                            )
                        return None

                if self.register_table.registers[self.fi.name] == self.name:
                    self.register_table.registers[self.fi.name] = None

            # Clear FU
            self.busy = False
            finished_instruction = self.instruction
            self.instruction = None
            self.op = None
            self.fi = None
            self.fj = None
            self.fk = None
            self.qj = None
            self.qk = None
            self.rj = False
            self.rk = False
            self.state = "Issue"
            self.op_cycle = 0

            # Need to update other FUs waiting for this result
            return (finished_instruction, "Write")

        return None

    def __len__(self):
        return len(self.instructions)


class Scoreboard:
    def __init__(self):
        # dict: Instruction -> dict com Issue, Read, Execute, Write
        self.instruction_status = {}

    def finished(self):
        return all(
            status["Write"] is not None for status in self.instruction_status.values()
        )

    def add_entry(
        self,
        instr,
        issue=None,
        read=None,
        execute=None,
        write=None,
    ):
        self.instruction_status[instr] = {
            "Instruction/Cycle": instr.original_instr(),
            "Issue": issue,
            "Read": read,
            "Execute": execute,
            "Write": write,
        }

    def update_entry(self, instr, stage, cycle):
        """Atualiza um estágio (issue/read/execute/write) da instrução"""
        if instr in self.instruction_status:
            self.instruction_status[instr][stage] = cycle
        else:
            raise KeyError(f"Instrução {instr} não encontrada no scoreboard")

    def to_dataframe(self):
        # transforma o dict em lista de linhas
        return pd.DataFrame(list(self.instruction_status.values()))

    def to_markdown(self):
        return self.to_dataframe().to_markdown(index=False)


def load_fu_config(filename):
    fu_units = {}
    fu_counts = {
        "int": 0,
        "add": 0,
        "mult": 0,
        "div": 0,
    }
    with open(filename) as f:
        for line in f:
            name, count, cost = line.strip().split()
            for _ in range(int(count)):
                fu_counts[name] = fu_counts[name] + 1
                aux = name + str(fu_counts[name])
                fu_units[aux] = FunctionalUnit(aux, int(cost))

    return fu_units


def run_simulation(fu_config, source_code, detect_hazards=False):
    global hazard_detection, hazards
    hazard_detection = detect_hazards
    hazards = []

    funits = load_fu_config(fu_config)
    scoreboard = Scoreboard()
    cpu = CPU(funits, scoreboard=scoreboard)

    lexer = DSBLexer()
    parser = DSBParser()
    with open(source_code) as f:
        instructions = parser.parse(lexer.tokenize(f.read()))
    cpu.load_instructions(instructions)
    cpu.run()

    # return both the scoreboard and hazards list
    return scoreboard, hazards


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print(
            "Uso: python dsb.py <fu_config.txt> <arquivo.s> [-h for hazards] [--hide-scoreboard]"
        )
        sys.exit(1)

    detect_hazards = "-h" in sys.argv
    hide_scoreboard = "--hide-scoreboard" in sys.argv
    scoreboard, hazards = run_simulation(sys.argv[1], sys.argv[2], detect_hazards)

    if detect_hazards and hazards:
        print("Hazards detected during execution:")
        for hazard in dict.fromkeys(hazards):  # dedup preserve order
            print(f"- {hazard}")
        print()

    if not hide_scoreboard:
        print(scoreboard.to_markdown())
