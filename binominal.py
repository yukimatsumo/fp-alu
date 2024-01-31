import sympy

# N = 2**10 #1e3
# P = 1e-3
# NP = N*P

# bin_coeff = sympy.binomial(N, NP)
# bin_p = bin_coeff*((P)**NP)*(1-P)**(N-NP)


N = 10
P = 10e-4
C = 1

# N = 256*10e4
# P = 10e-4
# C = 256

bin_coeff = sympy.binomial(N, C)
bin_p = bin_coeff*((P)**C)*(1-P)**(N-C)
print(bin_p)