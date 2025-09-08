## Hazards detected during execution:
- RAW hazard: (instruction: 3) fdiv f2, f4, f5 cannot read f5 because it is being written by another instruction.

## Scoreboard:
| Instruction/Cycle   |   Issue |   Read |   Execute |   Write |
|:--------------------|--------:|-------:|----------:|--------:|
| fld f1, x1          |       1 |      2 |         3 |       4 |
| fld f5, x1          |       2 |      3 |         4 |       5 |
| fdiv f2, f4, f5     |       3 |      6 |        16 |      17 |
