## Hazards detected during execution:
- Structural hazard: No available functional unit (add) for instruction fsub f8, f4, f2 (instruction: 3)
- RAW hazard: (instruction: 2) fadd f4, f2, f6 cannot read f2 because it is being written by another instruction.

## Scoreboard:
| Instruction/Cycle   |   Issue |   Read |   Execute |   Write |
|:--------------------|--------:|-------:|----------:|--------:|
| fld f2, x1          |       1 |      2 |         3 |       4 |
| fadd f4, f2, f6     |       2 |      5 |         7 |       8 |
| fsub f8, f4, f2     |       9 |     10 |        12 |      13 |
