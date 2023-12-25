class Ugate:
    def __init__(self):
        self.n_AND = 0
        self.n_OR = 0
        self.n_NOT = 0
        self.n_NAND = 0
        self.n_NOR = 0
        self.n_XOR = 0
        self.n_DFF = 0
        
    def AND(self, a :bool, b :bool) -> bool:
        self.n_AND += 1
        return a & b

    def OR(self, a :bool, b :bool) -> bool:
        self.n_OR += 1
        return a | b

    def NOT(self, a :bool) -> bool:
        self.n_NOT += 1
        # return not a
        return 0 if a == 1 else 1

    def NAND(self, a :bool, b :bool) -> bool:
        self.n_NAND += 1
        # return not (a & b)
        return self.NOT(self.AND(a, b))
    
    def NOR(self, a :bool, b :bool) -> bool:
        self.n_NOR += 1
        # return not (a | b)
        return self.NOT(self.OR(a, b))
    
    def XOR(self, a :bool, b :bool) -> bool:
        self.n_XOR += 1
        # return (a & (not b)) | ((not a) & b)
        # return  (a | b) & (not (a & b))
        return self.AND(self.OR(a, b), self.NAND(a, b))
    
    def MUX(self, a :bool, b :bool, c :bool) -> bool:
        """ return (a & (not c)) | (b & c) """
        return self.OR(self.AND(a, self.NOT(c)), self.AND(b, c))
    
    # boolean version
    def bNAND(self, a :bool, b :bool) -> bool:
        self.n_NAND += 1
        return not (a & b)
    
    def bNOR(self, a :bool, b :bool) -> bool:
        self.n_NOR += 1
        return not (a | b)
    
    def bAND(self, a :bool, b :bool) -> bool:
        self.n_AND += 1
        return not self.bNAND(a, b)

    def bOR(self, a :bool, b :bool) -> bool:
        self.n_OR += 1
        return not self.bNOR(a, b)

    def bNOT(self, a :bool) -> bool:
        self.n_NOT += 1
        return not a
    
    def bXOR(self, a :bool, b :bool) -> bool:
        self.n_XOR += 1
        # return (a & (not b)) | ((not a) & b)
        # return  (a | b) & (not (a & b))
        return self.bOR(self.bAND(a, self.bNOT(b)), self.bAND(self.bNOT(a), b))
        # return self.AND(self.OR(a, b), self.NAND(a, b))

    def bDFF(self, a :bool) -> bool:
        self.n_DFF += 1
        return a