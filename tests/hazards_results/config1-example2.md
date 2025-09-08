## Hazards detected during execution:
- WAW hazard: (instruction: 3) fadd f2, f1, f3 cannot write to f2 because it is already being written by another instruction.
- Structural hazard: No available functional unit (add) for instruction fsub f6, f3, f4 (instruction: 6)
- RAW hazard: (instruction: 6) fsub f6, f3, f4 cannot read f3 because it is being written by another instruction.
- Structural hazard: No available functional unit (add) for instruction fadd f4, f5, f2 (instruction: 8)

## Scoreboard:
| Instruction/Cycle   |   Issue |   Read |   Execute |   Write |
|:--------------------|--------:|-------:|----------:|--------:|
| fld f1, 100(x7)     |       1 |      2 |         3 |       4 |
| fmul f2, f2, f4     |       2 |      3 |         7 |       8 |
| fadd f2, f1, f3     |       9 |     10 |        12 |      13 |
| fld f9, x3          |      10 |     11 |        12 |      13 |
| fdiv f3, f1, f7     |      11 |     12 |        22 |      23 |
| fsub f6, f3, f4     |      14 |     24 |        26 |      27 |
| fmul f7, f1, f2     |      15 |     16 |        20 |      21 |
| fadd f4, f5, f2     |      28 |     29 |        31 |      32 |
| fsd f1, 50(x11)     |      29 |     30 |        31 |      32 |
