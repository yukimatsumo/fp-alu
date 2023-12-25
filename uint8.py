import numpy as np
from typing import Tuple

from util import *
from gate_e import *
# from gate import *

class Uint8(Ugate):
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
    
    # def csa_array(self, a, b, s, c) -> Tuple[bool, bool]:
    #     # Carry Save Adder
    #     return self.fadd(self.AND(a, b), s, c)

    def ui8add(self, a: str, b: str) -> str:
        self.nbit = 8
        # 8bit x 8bit unsigned integer addition
        if len(a) != self.nbit or len(b) != self.nbit:
            raise ValueError('a or b is not 8bit')
        a7, a6, a5, a4, a3, a2, a1, a0 = separate8(a)
        b7, b6, b5, b4, b3, b2, b1, b0 = separate8(b)
        c0, s0 = self.hadd(a0, b0)
        c1, s1 = self.fadd(a1, b1, c0)
        c2, s2 = self.fadd(a2, b2, c1)
        c3, s3 = self.fadd(a3, b3, c2)
        c4, s4 = self.fadd(a4, b4, c3)
        c5, s5 = self.fadd(a5, b5, c4)
        c6, s6 = self.fadd(a6, b6, c5)
        c,  s7 = self.fadd(a7, b7, c6)
        return concat9([c, s7, s6, s5, s4, s3, s2, s1, s0])
        
    def _ui8add(self, uint8_a: UINT8, uint8_b: UINT8) -> Tuple[UINT8, str]:
        self.__init__(nbit=8)
        # 8bit x 8bit unsigned integer addition
        if uint8_a > (2**self.nbit) -1  or uint8_b > (2**self.nbit) -1:
            raise ValueError('uint8_a or uint8_b is out of range')
        a = d_to_bin(uint8_a, self.nbit)
        b = d_to_bin(uint8_b, self.nbit)
        res = self.ui8add(a, b)
        return bin_to_d(res), res
    
    def ui8mul(self, a: str, b: str) -> str:
        self.nbit = 8
        # 8bit x 8bit unsigned integer multiplication
        if len(a) != self.nbit or len(b) != self.nbit:
            raise ValueError('a or b is not 8bit')
        a7, a6, a5, a4, a3, a2, a1, a0 = separate8(a)
        b7, b6, b5, b4, b3, b2, b1, b0 = separate8(b)
        c00, p0  = self.csa(a0, b0, 0, 0)
        c01, s01 = self.csa(a0, b1, 0, 0)
        c02, s02 = self.csa(a0, b2, 0, 0)
        c03, s03 = self.csa(a0, b3, 0, 0)
        c04, s04 = self.csa(a0, b4, 0, 0)
        c05, s05 = self.csa(a0, b5, 0, 0)
        c06, s06 = self.csa(a0, b6, 0, 0)
        c07, s07 = self.csa(a0, b7, 0, 0)
        c10, p1  = self.csa(a1, b0, s01, c00)
        c11, s11 = self.csa(a1, b1, s02, c01)
        c12, s12 = self.csa(a1, b2, s03, c02)
        c13, s13 = self.csa(a1, b3, s04, c03)
        c14, s14 = self.csa(a1, b4, s05, c04)
        c15, s15 = self.csa(a1, b5, s06, c05)
        c16, s16 = self.csa(a1, b6, s07, c06)
        c17, s17 = self.csa(a1, b7, 0, c07)
        c20, p2  = self.csa(a2, b0, s11, c10)
        c21, s21 = self.csa(a2, b1, s12, c11)
        c22, s22 = self.csa(a2, b2, s13, c12)
        c23, s23 = self.csa(a2, b3, s14, c13)
        c24, s24 = self.csa(a2, b4, s15, c14)
        c25, s25 = self.csa(a2, b5, s16, c15)
        c26, s26 = self.csa(a2, b6, s17, c16)
        c27, s27 = self.csa(a2, b7, 0, c17)
        c30, p3  = self.csa(a3, b0, s21, c20)
        c31, s31 = self.csa(a3, b1, s22, c21)
        c32, s32 = self.csa(a3, b2, s23, c22)
        c33, s33 = self.csa(a3, b3, s24, c23)
        c34, s34 = self.csa(a3, b4, s25, c24)
        c35, s35 = self.csa(a3, b5, s26, c25)
        c36, s36 = self.csa(a3, b6, s27, c26)
        c37, s37 = self.csa(a3, b7, 0, c27)
        c40, p4  = self.csa(a4, b0, s31, c30)
        c41, s41 = self.csa(a4, b1, s32, c31)
        c42, s42 = self.csa(a4, b2, s33, c32)
        c43, s43 = self.csa(a4, b3, s34, c33)
        c44, s44 = self.csa(a4, b4, s35, c34)
        c45, s45 = self.csa(a4, b5, s36, c35)
        c46, s46 = self.csa(a4, b6, s37, c36)
        c47, s47 = self.csa(a4, b7, 0, c37)
        c50, p5  = self.csa(a5, b0, s41, c40)
        c51, s51 = self.csa(a5, b1, s42, c41)
        c52, s52 = self.csa(a5, b2, s43, c42)
        c53, s53 = self.csa(a5, b3, s44, c43)
        c54, s54 = self.csa(a5, b4, s45, c44)
        c55, s55 = self.csa(a5, b5, s46, c45)
        c56, s56 = self.csa(a5, b6, s47, c46)
        c57, s57 = self.csa(a5, b7, 0, c47)
        c60, p6  = self.csa(a6, b0, s51, c50)
        c61, s61 = self.csa(a6, b1, s52, c51)
        c62, s62 = self.csa(a6, b2, s53, c52)
        c63, s63 = self.csa(a6, b3, s54, c53)
        c64, s64 = self.csa(a6, b4, s55, c54)
        c65, s65 = self.csa(a6, b5, s56, c55)
        c66, s66 = self.csa(a6, b6, s57, c56)
        c67, s67 = self.csa(a6, b7, 0, c57)
        c70, p7  = self.csa(a7, b0, s61, c60)
        c71, s71 = self.csa(a7, b1, s62, c61)
        c72, s72 = self.csa(a7, b2, s63, c62)
        c73, s73 = self.csa(a7, b3, s64, c63)
        c74, s74 = self.csa(a7, b4, s65, c64)
        c75, s75 = self.csa(a7, b5, s66, c65)
        c76, s76 = self.csa(a7, b6, s67, c66)
        c77, s77 = self.csa(a7, b7, 0, c67)
        c80, p8  = self.fadd(0, s71, c70)
        c81, p9  = self.fadd(c80, s72, c71)
        c82, p10 = self.fadd(c81, s73, c72)
        c83, p11 = self.fadd(c82, s74, c73)
        c84, p12 = self.fadd(c83, s75, c74)
        c85, p13 = self.fadd(c84, s76, c75)
        c86, p14 = self.fadd(c85, s77, c76)
        c,   p15 = self.fadd(c86, 0, c77)
        return concat16([p15, p14, p13, p12, p11, p10, p9, p8, p7, p6, p5, p4, p3, p2, p1, p0, c])

    def _ui8mul(self, uint8_a: UINT8, uint8_b: UINT8) -> Tuple[UINT8, str]:
        self.__init__(nbit=8)
        # 8bit x 8bit unsigned integer multiplication
        if uint8_a > (2**self.nbit) -1 or uint8_b > (2**self.nbit) -1:
            raise ValueError('uint8_a or uint8_b is out of range')
        a = d_to_bin(uint8_a, self.nbit)
        b = d_to_bin(uint8_b, self.nbit)
        res = self.ui8mul(a, b)
        return bin_to_d(res), res

def main():
    g = Uint8()

    # for i in range(0, 256):
    #     for j in range(0, i+1):
    #         d, b = g._ui8mul(i, j)
    #         if b[0] != "1" and b[9] != "0":
    #             print(f"{i:>3} x {j:>3} = {d:>5} ({b})")

    for i in range(0, 256):
        for j in range(0, 256):
            d, b = g._ui8mul(i, j)
            print(f"{i:>3} x {j:>3} = {d:>5} ({b})")

if __name__ == '__main__':
    main()