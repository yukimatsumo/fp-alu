import argparse
from typing import Tuple

from util import *
from uint import Uint

def __get_args():
    descri = 'floating point calculation module'
    parser = argparse.ArgumentParser(description=descri)
    parser.add_argument('-t', '--type', help='fp data type to be calculated', default="bfloat16", type=str)
    return parser.parse_args()

# param_dict = {"float128": [128, 15, 112, 16385], "float64": [64, 11, 52, 1025], "float32": [32, 8, 23, 129], "float16": [16, 5, 10, 17], "bfloat16": [16, 8, 7, 129]}

class Fp(Uint):
    def __init__(self, fp_type :str):
        self.fp_type = fp_type
        self.len_fp = param_dict[self.fp_type][0]
        self.len_exp = param_dict[self.fp_type][1]
        self.len_frac = param_dict[self.fp_type][2]
        self.bias = d_to_bin(param_dict[self.fp_type][3], self.len_exp)
        super().__init__(nbit=self.len_frac +1)
        self.init = True
        
    def init__(self):
        self.init = False
        self.n_AND = 0
        self.n_OR = 0
        self.n_NOT = 0
        self.n_NAND = 0
        self.n_NOR = 0
        self.n_XOR = 0
        self.v_add = None
        self.v_mul = None
        self.v_norm = None
        self.v_round = None
        self.cn = None
        self.cr = None

    def __str__(self):
        if self.init:
            self.init__()
        res = f"fp_type: {self.fp_type}, len_fp: {self.len_fp}, len_exp: {self.len_exp}, len_frac: {self.len_frac}, bias: {self.bias}\n"
        res = res + f"v_add: {self.v_add}, v_mul: {self.v_mul}, v_norm: {self.v_norm}, v_round: {self.v_round}, cn: {self.cn}, cr: {self.cr}\n"   
        return res + super().__str__()
    
    def str__(self): # TODO: wrapper for countig gates
        print(super().__str__())
    
    def __repr__(self):
        return f"Fp({self.fp_type})"

    def hbr(self, frac :str):
        # Hidden  bit  restor
        return "1" + frac

    def hbo(self, v_round :str):
        # Hidden bit omit
        return v_round[1:]

    def mux_rshift(self, binary: str) -> str:
        # 1 bit Right shift for n-bit binary with MUX
        l = len(binary)
        res = str(self.MUX(B(binary[0]), 0, B(binary[0])))
        for i in range(l-1):
            res = res + str(self.MUX(B(binary[i+1]), B(binary[i]), B(binary[0])))
        return res

    def normalize(self, binary: str) -> Tuple[bool, str]:
        # Normalize binary to 1.xxxxxx (raange of x is 0 to 1)
        res = self.mux_rshift(binary)
        return B(binary[0]), res[1:]

    def zero_judge(self, binary: str) -> bool:
        # zero judge
        l = len(binary) -1
        buf = self.OR(B(binary[0]), B(binary[1]))
        for i in range(1, l):
            buf = self.OR(buf, B(binary[i+1]))
        return buf

    def round(self, binary: str) -> Tuple[bool, str]:
        # Round to n-bit (RNE: round to nearest even)
        i_lsb = self.len_frac
        i_guard = self.len_frac +1
        i_round = self.len_frac +2
        i_sticky = self.len_frac +3
        lsb = binary[i_lsb]
        g = binary[i_guard]
        r = binary[i_round]
        s = self.zero_judge(binary[i_sticky:])
        round_op = self.AND(B(g), self.OR(self.OR(B(lsb), B(r)), B(s)))
        return self.rca(binary[:i_lsb +1], d_to_bin(round_op, i_lsb +1))

    def fp_add(self, binary_a: str, binary_b: str) -> str: ...
        # floating point addition

    def _fp_add(self, a: FLOAT, b: FLOAT) -> Tuple[FLOAT, str]: ...
        # floating point addition

    def fp_mul(self, binary_a: str, binary_b: str) -> str:
        self.init__()
        # floating point multiplication
        sign_a, exp_a, frac_a = decode_fp(binary_a, self.fp_type)
        sign_b, exp_b, frac_b = decode_fp(binary_b, self.fp_type)
        # sign part
        sign = self.XOR(B(sign_a), B(sign_b))
        # exponent addition
        _, v_add = self.rca(exp_a, exp_b)
        check, self.v_add = self.rca(v_add, self.bias) # sutraction of bias
        if check:
            raise ValueError("overflow")
        # fraction multiplication -> normalization -> rounding
        self.v_mul = self.umul(self.hbr(frac_a), self.hbr(frac_b))
        self.cn, self.v_norm = self.normalize(self.v_mul)
        self.cr, self.v_round = self.round(self.v_norm)
        frac = self.hbo(self.v_round)
        # adjust exponent (carry addition to exponent)
        c, s = self.hadd(self.cn, self.cr)
        check, exp = self.rca(self.v_add, d_to_bin(B(c)+B(s), self.len_exp))
        if check:
            raise ValueError("overflow")
        return str(sign) + exp + frac
    
    def _fp_mul(self, a: FLOAT, b: FLOAT) -> Tuple[FLOAT, str]: #FIXME: date check
        self.init__()
        # floating point multiplication
        if a == np.nan or b == np.nan:
            raise ValueError("NaN is not supported")
        elif np.isinf(a) or np.isinf(b):
            raise ValueError("infinity is not supported")
        elif a == 0 or b == 0:
            res = '0' * self.len_fp
        else:
            res = self.fp_mul(d_to_fp(a, self.fp_type), d_to_fp(b, self.fp_type))
        return b_to_fp(res, self.fp_type)[2], res

class Bfloat16(Fp):
    def __init__(self):
        super().__init__(fp_type="bfloat16")

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return f"Bfloat16()"
    
    def bf16_add(self, binary_a: str, binary_b: str) -> str: ...
        # Bfloat16 addition

    def _bf16_add(self, a: BFLOAT16, b: BFLOAT16) -> Tuple[BFLOAT16, str]: ...
        # Bfloat16 addition

    def bf16_mul(self, binary_a: str, binary_b: str) -> str:
        # self.__init__()
        return self.fp_mul(binary_a, binary_b)
    
    def _bf16_mul(self, a: BFLOAT16, b: BFLOAT16) -> Tuple[BFLOAT16, str]:
        # self.__init__()
        return self._fp_mul(a, b)

class Fp16(Fp):
    def __init__(self):
        super().__init__(fp_type="float16")

class Fp32(Fp):
    def __init__(self):
        super().__init__(fp_type="float32")

def main():
    args = __get_args()
    g = Bfloat16()
    h = Fp(args.type)

    for i in range(127, 128):
        for j in range(128):
            a = g._bf16_mul(i, j)
            b = h._fp_mul(i, j)
            if a != b:
                print(a, b)

    print(g)
    print(h)


if __name__ == '__main__':
    main()