import argparse, math
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
import jj_model

VB = 2.5e-3 #[V]
FREQ = 1.0e9 #[Hz]
TASKCC = 1.0e9 #[CC]

def __get_args():
    descri = 'estimaton of effect of DVFS on SFQ & HFQ circuits'
    parser = argparse.ArgumentParser(description=descri)
    parser.add_argument('-t', '--type', help='sfq or hfq', default="sfq", type=str)
    return parser.parse_args()

def dvfs_sfq() -> None:
    pass

def dvfs_hfq() -> None:
    pass

def main() -> None:
    args = __get_args()
    dvfs_sfq()
    dvfs_hfq()
    jj_model.profier(area=2.16, betac=1.0, vb=VB)
    
    
if __name__ == "__main__":
    main()
    print('Hello World!')
    