import numpy as np
from typing import Tuple

from util import *
from gate import *

class Uint4(Ugate):
    def __init__(self, nbit=8):
        super().__init__()
        self.nbit = nbit
    
    def fadd(self, a :bool, b :bool, c :bool) -> Tuple[bool, bool]:
        # Full Adder
        m1= self.XOR(a, b)
        m2 = self.AND(a, b)
        s = self.XOR(m1, c)
        c = self.OR(self.AND(m1, c), m2)
        return c, s
    
    def hadd(self, a :bool, b :bool) -> Tuple[bool, bool]:
        # Half Adder
        return self.fadd(a, b, 0)
    
    def csa(self, a :bool, b :bool, s :bool, c :bool) -> Tuple[bool, bool]:
        # Carry Save Adder
        return self.fadd(self.AND(a, b), s, c)
    
    def ui4add_s(self, a: str, b: str) -> str:
        self.nbit = 4
        # 4bit x 4bit unsigned integer addition
        if len(a) != self.nbit or len(b) != self.nbit:
            raise ValueError('a or b is not 4bit')
        a3, a2, a1, a0 = separate4(a)
        b3, b2, b1, b0 = separate4(b)
        c0, s0 = self.hadd(a0, b0)
        c1, s1 = self.fadd(a1, b1, c0)
        c2, s2 = self.fadd(a2, b2, c1)
        c,  s3 = self.fadd(a3, b3, c2)
        return concat5([c, s3, s2, s1, s0])

    def ui4add(self, uint4_a: UINT4, uint4_b: UINT4) -> Tuple[UINT4, str]:
        self.__init__(nbit=4)
        # 4bit x 4bit unsigned integer addition
        if uint4_a > (2**self.nbit) -1  or uint4_b > (2**self.nbit) -1:
            raise ValueError('uint4_a or uint4_b is out of range')
        a = d_to_bin(uint4_a, self.nbit)
        b = d_to_bin(uint4_b, self.nbit)
        res = self.ui4add_s(a, b)
        return bin_to_d(res), res
    
    def ui4mul_s(self, a: str, b: str) -> str:
        self.nbit = 4
        # 4bit x 4bit unsigned integer multiplication
        if len(a) != self.nbit or len(b) != self.nbit:
            raise ValueError('a or b is not 4bit')
        a3, a2, a1, a0 = separate4(a)
        b3, b2, b1, b0 = separate4(b)
        c00, p0  = self.csa(a0, b0, 0, 0)
        c01, s01 = self.csa(a0, b1, 0, 0)
        c02, s02 = self.csa(a0, b2, 0, 0)
        c03, s03 = self.csa(a0, b3, 0, 0)
        c10, p1  = self.csa(a1, b0, s01, c00)
        c11, s11 = self.csa(a1, b1, s02, c01)
        c12, s12 = self.csa(a1, b2, s03, c02)
        c13, s13 = self.csa(a1, b3, 0, c03)
        c20, p2  = self.csa(a2, b0, s11, c10)
        c21, s21 = self.csa(a2, b1, s12, c11)
        c22, s22 = self.csa(a2, b2, s13, c12)
        c23, s23 = self.csa(a2, b3, 0, c13)
        c30, p3  = self.csa(a3, b0, s21, c20)
        c31, s31 = self.csa(a3, b1, s22, c21)
        c32, s32 = self.csa(a3, b2, s23, c22)
        c33, s33 = self.csa(a3, b3, 0, c23)
        c40, p4  = self.fadd(0, s31, c30)
        c41, p5  = self.fadd(c40, s32, c31)
        c42, p6  = self.fadd(c41, s33, c32)
        c,   p7  = self.fadd(c42, 0, c33)
        return concat8([p7, p6, p5, p4, p3, p2, p1, p0])
    
    def ui4mul(self, uint4_a: UINT4, uint4_b: UINT4) -> Tuple[UINT4, str]:
        self.__init__(nbit=4)
        # 4bit x 4bit unsigned integer multiplication
        if uint4_a > (2**self.nbit) -1 or uint4_b > (2**self.nbit) -1:
            raise ValueError('uint4_a or uint4_b is out of range')
        a = d_to_bin(uint4_a, self.nbit)
        b = d_to_bin(uint4_b, self.nbit)
        res = self.ui4mul_s(a, b)
        return bin_to_d(res), res

def main():
    g = Uint4()
    for i in range(0, 16):
        for j in range(15, 16):
            print(i, " + ", j, " = ", g.ui4add(i, j))

    for i in range(0, 16):
        for j in range(15, 16):
            print(i, " x ", j, " = ", g.ui4mul(i, j))

if __name__ == '__main__':
    main()