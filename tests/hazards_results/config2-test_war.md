## Hazards detected during execution:
- WAW hazard: (instruction: 4) fadd f2, f5, f8 cannot write to f2 because it is already being written by another instruction.
- RAW hazard: (instruction: 3) fmul f4, f2, f6 cannot read f6 because it is being written by another instruction.
- RAW hazard: (instruction: 5) fsd f2, x1 cannot read f2 because it is being written by another instruction.
- WAR hazard: (instruction: 4) fadd f2, f5, f8 cannot write to f2 because fmul f4, f2, f6 needs to read it.

## Scoreboard:
| Instruction/Cycle   |   Issue |   Read |   Execute |   Write |
|:--------------------|--------:|-------:|----------:|--------:|
| fld f2, x1          |       1 |      2 |         3 |       4 |
| fdiv f6, f9, f3     |       2 |      3 |        13 |      14 |
| fmul f4, f2, f6     |       3 |     15 |        19 |      20 |
| fadd f2, f5, f8     |       5 |      6 |         8 |      16 |
| fsd f2, x1          |       6 |     17 |        18 |      19 |
