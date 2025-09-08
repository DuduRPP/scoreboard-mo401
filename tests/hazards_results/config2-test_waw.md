## Hazards detected during execution:
- WAW hazard: (instruction: 2) fdiv f2, f1, f3 cannot write to f2 because it is already being written by another instruction.
- WAW hazard: (instruction: 4) fmul f4, f1, f3 cannot write to f4 because it is already being written by another instruction.
- Structural hazard: No available functional unit (int) for instruction fsd f4, 64(x10) (instruction: 6)
- RAW hazard: (instruction: 5) fsd f2, 32(x10) cannot read f2 because it is being written by another instruction.

## Scoreboard:
| Instruction/Cycle   |   Issue |   Read |   Execute |   Write |
|:--------------------|--------:|-------:|----------:|--------:|
| fld f2, x1          |       1 |      2 |         3 |       4 |
| fdiv f2, f1, f3     |       5 |      6 |        16 |      17 |
| fld f4, 128(x2)     |       6 |      7 |         8 |       9 |
| fmul f4, f1, f3     |      10 |     11 |        15 |      16 |
| fsd f2, 32(x10)     |      11 |     18 |        19 |      20 |
| fsd f4, 64(x10)     |      21 |     22 |        23 |      24 |
