from typing import Tuple

from util import *
from gate import *

class Compare(Ugate):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        self.sfq_AND = self.n_AND - self.n_XOR*2
        self.sfq_OR = self.n_OR - self.n_XOR
        self.sfq_NOT = self.n_NOT - self.n_XOR*2
        self.sfq_XOR = self.n_XOR
        res = f"SFQ-AND: {self.sfq_AND}, SFQ-OR: {self.sfq_OR}, SFQ-NOT: {self.sfq_NOT}, SFQ-XOR: {self.sfq_XOR}, SFQ-DFF: {self.n_DFF}"
        return res
    
    def __repr__(self) -> str:
        return f"Compare()"

    def compare_int(self, a: int, b: int) -> bool:
        return a > b
    
    def not_a_gt_b(self, a: bool, b: bool) -> Tuple[bool, bool]:
        not_a_gt_b = self.bOR(self.bNOT(a), self.bDFF(b))
        not_a_eq_b = self.bXOR(self.bDFF(a), self.bDFF(b))
        return not_a_gt_b, not_a_eq_b
    
    def compare_1bit(self, a: bool, b: bool) -> Tuple[bool, bool, bool]:
        not_a_gt_b, not_a_eq_b = self.not_a_gt_b(a, b)
        a_gt_b = self.bNOT(not_a_gt_b)
        a_eq_b = self.bNOT(not_a_eq_b)
        a_lt_b = self.bAND(not_a_eq_b, not_a_gt_b)
        return a_gt_b, a_eq_b, a_lt_b
            
    def compare_mbit(self, a: str, b: str) -> Tuple[bool, bool, bool]:
        self.__init__()
        if len(a) != len(b):
            raise ValueError("len(a) must be equal to len(b)")
        n = len(a)
        bool_a = [True if a[i] == '1' else False for i in range(n)]
        bool_b = [True if b[i] == '1' else False for i in range(n)]
        not_a_gt_b_i = [False] * n
        not_a_eq_b_i = [False] * n
        for i in range(n):
            not_a_gt_b_i[i], not_a_eq_b_i[i] = self.not_a_gt_b(bool_a[i], bool_b[i])
            if i > 1:
                for _ in range(i-1):
                    not_a_gt_b_i[i] = self.bDFF(not_a_gt_b_i[i])
                    not_a_eq_b_i[i] = self.bDFF(not_a_eq_b_i[i])


        not_a_gt_b = self.bDFF(not_a_gt_b_i[0]) if n > 1 else not_a_gt_b_i[0]
        not_a_eq_b = not_a_eq_b_i[0]
        for i in range(1, n):
            buf = self.bOR(not_a_eq_b, not_a_gt_b_i[i])
            not_a_gt_b = self.bAND(not_a_gt_b, buf)
            not_a_eq_b = self.bOR(not_a_eq_b, not_a_eq_b_i[i])
            
        not_a_eq_b = self.bDFF(not_a_eq_b)
        a_gt_b = self.bNOT(not_a_gt_b)
        a_eq_b = self.bNOT(not_a_eq_b)
        a_lt_b = self.bAND(not_a_eq_b, not_a_gt_b)
        return a_gt_b, a_eq_b, a_lt_b

def main() -> None:
    g = Compare()
    for n in range(1, 9):
        # check = [False, False, False] * ((2 ** n) ** 2)
        for i in range(2**n):
            for j in range(2**n):
                check = [False, False, False]
                if i > j:
                    check[0] = True
                elif i == j:
                    check[1] = True
                else:
                    check[2] = True
                ans = g.compare_mbit(d_to_bin(i, n), d_to_bin(j, n))
                if list(ans) != check:
                    print(f"Error: {i}, {j}")
                    exit(1)
        print(f"{g}\n")

if __name__ == "__main__":
    main()