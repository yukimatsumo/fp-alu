import sympy

# N = 2**10 #1e3
# P = 1e-3
# NP = N*P

N = 10
P = 1/2
NP = 5 

bin_coeff = sympy.binomial(N, NP)
bin_p = bin_coeff*((P)**NP)*(1-P)**(N-NP)
print(bin_p)