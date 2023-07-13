import argparse
from typing import Tuple

from util import *
from gate import *

def __get_args():
    descri = 'n-bit unsigened integer calculation module'
    parser = argparse.ArgumentParser(description=descri)
    parser.add_argument('-n', '--nbit', help='bit length of data to be calculated', default=8, type=int)
    return parser.parse_args()

class Uint(Ugate):
    def __init__(self, nbit :int):
        super().__init__()
        self.nbit = nbit

    def __str__(self):
        self.sfq_AND = self.n_AND - self.n_XOR*2
        self.sfq_OR = self.n_OR - self.n_XOR
        self.sfq_NOT = self.n_NOT - self.n_XOR
        self.sfq_XOR = self.n_XOR
        res = f"AND: {self.n_AND}, OR: {self.n_OR}, NOT: {self.n_NOT}, NAND: {self.n_NAND}, NOR: {self.n_NOR}, XOR: {self.n_XOR}\n"
        res = res + f"SFQ-AND: {self.sfq_AND}, SFQ-OR: {self.sfq_OR}, SFQ-NOT: {self.sfq_NOT}, SFQ-XOR: {self.sfq_XOR}"
        return res
    
    def __repr__(self):
        return f"Uint({self.nbit})"
    
    def fadd(self, a :bool, b :bool, ci :bool) -> Tuple[bool, bool]:
        # Full Adder
        m1= self.XOR(a, b)
        m2 = self.AND(a, b)
        s = self.XOR(m1, ci)
        m3 = self.AND(m1, ci)
        c = self.OR(m2, m3)
        return c, s
    
    def hadd(self, a :bool, b :bool) -> Tuple[bool, bool]:
        # Half Adder
        return self.fadd(a, b, 0)
    
    def csa(self, a :bool, b :bool, s :bool, c :bool) -> Tuple[bool, bool]:
        # Carry Save Adder
        return self.fadd(self.AND(a, b), s, c)
    
    def csa_array(self, a :bool, b :str, si :str, ci :str) -> Tuple[str, str]:
        # Carry Save Adder Array
        l = len(b)
        c_stream = ""
        s_stream = "0"
        for i in range(l):
            c, s = self.csa(a, B(b[i]), B(si[i]), B(ci[i]))
            c_stream = c_stream + str(c)
            s_stream = s_stream + str(s)
        return c_stream, s_stream
    
    def csa_matrix(self, a :str, b :str) -> Tuple[str, str, str]:
        # Carry Save Adder Matrix
        l = len(a)
        c_stream = '0' * (112+1) # TODO: move to global variable
        s_stream = '0' + c_stream
        p_stream = ""
        for i in range(l-1, -1, -1):
            c_stream, s_stream = self.csa_array(B(a[i]), b, s_stream, c_stream)
            p_stream = s_stream[l] + p_stream
        return c_stream, s_stream, p_stream

    def rca(self, a :str, b :str) -> Tuple[bool, str]:
        # Ripple Carry Adder
        l = len(a)
        c, s = self.hadd(B(a[l-1]), B(b[l-1]))
        res = str(s)
        for i in range(l-1, 0, -1):
            c, s = self.fadd(B(a[i-1]), B(b[i-1]), c)
            res = str(s) + res
        return B(c), res
    
    def cla(self, a :str, b :str) -> Tuple[bool, str]: # FIXME: not working
        # Carry Look Ahead Adder
        l = len(a)
        g = [None] * l
        p = [None] * l
        g[0] = self.AND(a[0], b[0])
        p[0] = self.OR(a[0], b[0])
        for i in range(1, l):
            g[i] = self.AND(a[i], b[i])
            p[i] = self.OR(a[i], b[i])
            g[i] = self.OR(g[i], self.AND(g[i-1], p[i-1]))
            p[i] = self.AND(p[i], p[i-1])
        c = g[l-1]
        s = self.XOR(a[l-1], b[l-1])
        for i in range(l-2, -1, -1):
            c, s = self.fadd(a[i], b[i], c)
        return B(c), s

    def uadd(self, a: str, b: str) -> Tuple[bool, str]:
        # super().__init__()
        # n-bit x n-bit unsigned integer addition
        if len(a) != self.nbit or len(b) != self.nbit:
            raise ValueError(f'a or b is not {self.nbit}bit')
        return self.rca(a, b)
        
    def _uadd(self, a: UINT, b: UINT) -> Tuple[UINT, str]:
        # n-bit x n-bit unsigned integer addition
        if a > (2**self.nbit) -1  or b > (2**self.nbit) -1 or a < 0 or b < 0:
            raise ValueError(f'a or b is out of range {self.nbit}bit')
        a = d_to_bin(a, self.nbit)
        b = d_to_bin(b, self.nbit)
        c, s = self.uadd(a, b)
        return bin_to_d(str(c)+s), str(c)+s
    
    def umul(self, a: str, b: str) -> str:
        # super().__init__()
        # n-bit x n-bit unsigned integer multiplication
        if len(a) != self.nbit or len(b) != self.nbit:
            raise ValueError(f'a or b is not {self.nbit}bit')
        c_stream, s_stream, lohalf = self.csa_matrix(a, b)
        _, hohalf = self.rca(s_stream[0:self.nbit], c_stream)
        return hohalf + lohalf

    def _umul(self, a: UINT, b: UINT) -> Tuple[UINT, str]:
        # n-bit x n-bit unsigned integer multiplication
        if a > (2**self.nbit) -1 or b > (2**self.nbit) -1 or a < 0 or b < 0:
            raise ValueError('a or b is out of range')
        a = d_to_bin(a, self.nbit)
        b = d_to_bin(b, self.nbit)
        res = self.umul(a, b)
        return bin_to_d(res), res

    @time_measure
    def test(self):
        super().__init__()
        lower = 0 # upper-1
        upper = 2**self.nbit # 2^nbit
        self.n = 0
        # for i in range(upper-1, upper):
        #     for j in range(0, i+1):
        #         self.n += 1
        #         _, _ = self._uadd(i, j)
        #         #print(i, " + ", j, " = ", self._uadd(i, j))
        for i in range(lower, upper):
            for j in range(0, i+1):
                self.n += 1
                _, _ = self._umul(i, j)
                #print(i, " x ", j, " = ", self._umul(i, j))

def main():
    args = __get_args()
    g = Uint(args.nbit)
    t = g.test()
    print(f"    n: {g.n} [trials]")
    print(f"avg_t: {t[1]/g.n} [ns]")
    print(f"\n{g}\n")

if __name__ == '__main__':
    main()