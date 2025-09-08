## Hazards detected during execution:
- Structural hazard: No available functional unit (int) for instruction fld f3, 16(x1) (instruction: 3)
- WAW hazard: (instruction: 6) fadd f3, f1, f2 cannot write to f3 because it is already being written by another instruction.
- RAW hazard: (instruction: 5) fmul f5, f3, f4 cannot read f4 because it is being written by another instruction.
- WAW hazard: (instruction: 7) fld f3, 16(x1) cannot write to f3 because it is already being written by another instruction.
- WAR hazard: (instruction: 6) fadd f3, f1, f2 cannot write to f3 because fmul f5, f3, f4 needs to read it.
- Structural hazard: No available functional unit (add) for instruction fadd f9, f5, f4 (instruction: 10)
- RAW hazard: (instruction: 9) fdiv f4, f3, f1 cannot read f1 because it is being written by another instruction.
- RAW hazard: (instruction: 10) fadd f9, f5, f4 cannot read f4 because it is being written by another instruction.
- RAW hazard: (instruction: 11) fsd f9, x2 cannot read f9 because it is being written by another instruction.

## Scoreboard:
| Instruction/Cycle   |   Issue |   Read |   Execute |   Write |
|:--------------------|--------:|-------:|----------:|--------:|
| fld f1, x1          |       1 |      2 |         3 |       4 |
| fld f2, 8(x1)       |       2 |      3 |         4 |       5 |
| fld f3, 16(x1)      |       5 |      6 |         7 |       8 |
| fdiv f4, f1, f2     |       6 |      7 |        17 |      18 |
| fmul f5, f3, f4     |       7 |     19 |        23 |      24 |
| fadd f3, f1, f2     |       9 |     10 |        12 |      20 |
| fld f3, 16(x1)      |      21 |     22 |        23 |      24 |
| fadd f1, f1, f2     |      22 |     23 |        25 |      26 |
| fdiv f4, f3, f1     |      23 |     27 |        37 |      38 |
| fadd f9, f5, f4     |      27 |     39 |        41 |      42 |
| fsd f9, x2          |      28 |     43 |        44 |      45 |
