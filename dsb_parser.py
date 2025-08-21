from sly import Lexer, Parser
from typing import List

class Register:
    def __init__(self, name, reg_type):
        self.name = name
        self.reg_type = reg_type
    def __str__(self):
        return f"{self.reg_type} {self.name}"
    def __repr__(self):
        return self.__str__()

class Instruction:
    def __init__(self, op, reads=None, writes=None):
        self.op: str = op
        self.reads: List[Register] = reads or []   # source registers
        self.writes: List[Register] = writes or [] # target registers
    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
    def __repr__(self):
        return self.__str__()


class ArithInstr(Instruction):
    def __init__(self, op, rd, rs1, rs2):
        super().__init__(op, reads=[rs1, rs2], writes=[rd])
        self.rd: Register = rd
        self.rs1: Register = rs1
        self.rs2: Register = rs2


class LoadInstr(Instruction):
    def __init__(self, op, rd, base, imm):
        super().__init__(op, reads=[base], writes=[rd])
        self.rd: Register = rd
        self.base: Register = base
        self.imm: int = imm

class StoreInstr(Instruction):
    def __init__(self, op, rs, base, imm):
        super().__init__(op, reads=[rs, base], writes=[])
        self.rs: Register = rs
        self.base: Register = base
        self.imm: int = imm


class DSBLexer(Lexer):
    instr_tokens = { FREG, XREG, NUM, OP }
    literal_tokens = { COMMA, LPAREN, RPAREN }
    tokens = instr_tokens | literal_tokens
    ignore = " \t"

    # Literals
    COMMA = r','
    LPAREN = r'\('
    RPAREN = r'\)'

    # Tokens
    FREG = r'f[0-9]+'
    XREG = r'x[0-9]+'
    NUM = r'[+-]?[0-9]+'

    # List of supported operations
    OP_LIST = ['fld', 'fsd', 'fadd', 'fsub', 'fmul', 'fdiv']
    OP = r'(' + '|'.join(OP_LIST) + r')'

class DSBParser(Parser):
    tokens = DSBLexer.tokens

    @_('arith_instr')
    def instruction(self, p):
        return p.arith_instr

    @_('mem_instr')
    def instruction(self, p):
        return p.mem_instr

    # Arithmetic: fadd rd, rs1, rs2
    @_('OP FREG COMMA FREG COMMA FREG')
    def arith_instr(self, p):
        rd = Register(p.FREG0, 'float')
        rs1 = Register(p.FREG1, 'float')
        rs2 = Register(p.FREG2, 'float')
        return ArithInstr(p.OP, rd, rs1, rs2)

    # Memory: fld f1, 0(x2)
    @_('OP FREG COMMA NUM LPAREN XREG RPAREN')
    def mem_instr(self, p):
        # TODO: FUTURE POSSIBLE OPTIMIZATION IS ADDING DIFFERENT OPS TO DIFFERENT LEXERS
        if p.OP == 'fld':
            rd = Register(p.FREG, 'float')
            imm = int(p.NUM)
            rs = Register(p.XREG, 'int')
            return LoadInstr(p.OP, rd, rs, imm)
        elif p.OP == 'fsd':
            rs = Register(p.FREG, 'float')
            imm = int(p.NUM)
            rd = Register(p.XREG, 'int')
            return StoreInstr(p.OP, rs, rd, imm)

    # Memory: fld f1, x2
    @_('OP FREG COMMA XREG')
    def mem_instr(self, p):
        if p.OP == 'fld':
            rd = Register(p.FREG, 'float')
            rs = Register(p.XREG, 'int')
            return LoadInstr(p.OP, rd, rs, 0)
        elif p.OP == 'fsd':
            rs = Register(p.FREG, 'float')
            rd = Register(p.XREG, 'int')
            return StoreInstr(p.OP, rs, rd, 0)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python parser.py programa.s")
        sys.exit(1)

    filename = sys.argv[1]

    lexer = DSBLexer()
    parser = DSBParser()

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:   # pular linhas vazias
                continue
            instr = parser.parse(lexer.tokenize(line))
            print(line, "->",instr)
