# (a/b)*e + e/(a+b)

# structural hazard in loads by insuficient FUs
fld f1, 0(x1)       # load a
fld f2, 8(x1)       # load b
fld f3, 16(x1)      # load e

# RAW
fdiv f4, f1, f2     # f4 = a/b
fmul f5, f3, f4     # f5 = (a/b)*e

# forces WAR and WAW
fadd f3, f1, f2
fld f3, 16(x1)

# RAW
fadd f1, f1, f2     # f1 = (a+b)
fdiv f4, f3, f1     # f4 = e/(a+b)

fadd f9, f5, f4     # f9 = f5 + f4 = (a/b)*e + e/(a+b)
fsd f9, 0(x2)
