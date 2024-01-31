import argparse, math
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from util import SIstr

KB = 1.38e-23 #[J/K]
Q = 1.6e-19 #[C]
T = 4.2 #[K]
B = 1.0e12 #[Hz]

PHI = 2.068e-15 #[Wb]
VG = 2.8e-3 #[V]
CAP = 0.064e-12 #[F]
R0 = 100 #[ohm]
RN = 16 #[ohm]
JC = 100e-6 # 10 [kA/cm^2]

AREA = 1.00 
VB = 2.5e-3 #[V]
FREQ = 50e9 #[Hz]
TASKCC = 1.0e9 #[CC]
# IC = AREA*JC
# RB = VB/(0.7*IC)

def __get_args():
    descri = 'calculate parameters of SFQ & HFQ circuits'
    parser = argparse.ArgumentParser(description=descri)
    parser.add_argument('-t', '--type', help='sfq or hfq', default="sfq", type=str)
    return parser.parse_args()

def jj_resistance(area: float, betac: float = 1.0) -> float:
    cap = CAP*area
    ic = JC*area
    r_subgap = R0/area
    denomi = math.sqrt(2 * math.pi * ic * cap / (PHI * betac)) - 1/r_subgap
    r_shunt = 1/denomi
    r_all = r_shunt*r_subgap/(r_shunt + r_subgap)
    return r_shunt, r_all

def sfq_jtl_inductance(ic :float) -> float:
    return 0.5*PHI/ic

def sfq_latch_inductance(ic :float) -> float:
    return 1.5*PHI/ic

def sfq_power(vb :float, ic :float, freq :float) -> float:
    dynamic_p = ic*freq*PHI
    static_p = 0.7*ic*vb
    return  dynamic_p + static_p

def sfq_energy(total_p :float, freq : float, task_cc :float) -> float:
    return total_p*(task_cc/freq)

def thermal_noise_current(r :float, noise_freq :float) -> float:
    return math.sqrt(4*KB*T*noise_freq/r)

def shot_noise_current(vb :float, rb :float, noise_freq :float) -> float:
    return math.sqrt(2*Q*(vb/rb)*noise_freq)

def profier(area :float=AREA, vb :float=VB, betac :float=1.0) -> None:
    ic = area*JC
    rb = vb/(0.7*ic)
    print(f"Vsg: {SIstr(VG)}V, Jc: {SIstr(JC*1e8)}A/cm^2")
    print(f"Area Factor: {SIstr(area)}, Ic: {SIstr(JC*area)}A, (CAP: {SIstr(CAP*area)}F, Rn: {SIstr(RN/area)}ohm, R0: {SIstr(R0/area)}ohm)")
    print(f"Vb: {SIstr(vb)}V, Rb: {SIstr(rb)}ohm, (Ib: {SIstr(vb/rb)}A)")
    
    l = sfq_jtl_inductance(ic)
    print(f"JTL cell:: Inductance: {SIstr(l)}H, Rb/2: {SIstr(rb/2)}ohm")
    print()
    
    rs, ra = jj_resistance(area, betac=betac)
    print(f"Rs: {SIstr(rs)}ohm, Rjj: {SIstr(ra)}ohm")
    
    hs = area*rs
    ha = area*ra
    print(f"IcRs: {SIstr(hs)}V, (IcRa: {SIstr(ha)}V)")
    print()
    
    tn_rb = thermal_noise_current(rb/2, B)
    sn = shot_noise_current(vb, rb/2, B)
    print(f"Rb:: Thermal Noise In: {SIstr(tn_rb)}A, Shot Noise In: {SIstr(sn)}A")    

    tn_rn = thermal_noise_current(RN/area, B)
    tn_r0 = thermal_noise_current(R0/area, B)
    tn_rs = thermal_noise_current(rs, B)
    tn_ra = thermal_noise_current(ra, B)
    print(f"Rn:: Thermal Noise In: {SIstr(tn_rn)}A")
    print(f"R0:: Thermal Noise In: {SIstr(tn_r0)}A")
    print(f"Rs:: Thermal Noise In: {SIstr(tn_rs)}A")
    print(f"Ra:: Thermal Noise In: {SIstr(tn_ra)}A")
    print()
    
    p = sfq_power(vb, ic, FREQ)
    e = sfq_energy(p, FREQ, TASKCC)
    print(F"Power: {SIstr(p)}W, Energy: {SIstr(e)}J")


def main() -> None:
    args = __get_args()
    profier(area=2.16, vb=2.5e-3, betac=2)
    delta_e = 100*KB*T
    ln2 = math.log(2)
    print(f"delta_E: {SIstr(delta_e)}J")
    print(f"ln2: {ln2}")
    
    print(delta_e*ln2)
    
    ic = 0.158*JC
    print(ic)
    
    
if __name__ == "__main__":
    main()
    print()
    