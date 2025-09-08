## Hazards detected during execution:
- Structural hazard: No available functional unit (int) for instruction fld f5, x1 (instruction: 2)
- RAW hazard: (instruction: 3) fdiv f2, f4, f5 cannot read f5 because it is being written by another instruction.

## Scoreboard:
| Instruction/Cycle   |   Issue |   Read |   Execute |   Write |
|:--------------------|--------:|-------:|----------:|--------:|
| fld f1, x1          |       1 |      2 |         3 |       4 |
| fld f5, x1          |       5 |      6 |         7 |       8 |
| fdiv f2, f4, f5     |       6 |      9 |        19 |      20 |
