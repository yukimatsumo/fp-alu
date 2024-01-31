import argparse, time, math
from functools import wraps
import numpy as np
from numpy import unsignedinteger
from typing import Any, Tuple

def time_measure(func :Any) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        res = func(*args, **kwargs)
        elapsed_time = time.perf_counter_ns() - start
        print(f"{func.__name__} elapsed_time: {elapsed_time} [ns]")
        return res, elapsed_time
    return wrapper

def SIstr(num):
    l = math.log(num,10)
    if l >= 12:
        return '{:.0f}'.format(num*10**-12) + " T"
    elif 12 > l and l >= 9:
        return '{:.0f}'.format(num*10**-9) + " G"
    elif 9 > l and l >= 6:
        return '{:.0f}'.format(num*10**-6) + " M"
    elif 6 > l and l >= 3:
        return '{:.0f}'.format(num*10**-3) + " k"
    elif 3 > l and l >= 2:
        return '{:.0f}'.format(num) + " "
    elif 2 > l and l >= 1:
        return '{:.1f}'.format(num) + " " 
    elif l >= -1:
        return '{:.2f}'.format(num) + " "
    elif -1 > l and l >= -4:
        if num >= 1e-3:
            return '{:.2f}'.format(num*10**3) + " m"
        elif num < 1e-3:
            return '{:.0f}'.format(num*10**6) + " u"
    elif -4 > l and l >= -7:
        return '{:.2f}'.format(num*10**6) + " u"
    elif -7 > l and l >= -10:
        return '{:.2f}'.format(num*10**9) + " n"
    elif -10 > l and l >= -13:
        return '{:.2f}'.format(num*10**12) + " p"
    elif -13 > l and l >= -16:
        return '{:.2f}'.format(num*10**15) + " f"
    elif -16 > l and l >= -19:
        return '{:.2f}'.format(num*10**18) + " a"
    elif -19 > l and l >= -22:
        return '{:.2f}'.format(num*10**21) + " z"

# TODO: FIXME: B, UINT4, UINT8, UINT24, BFLOAT16, FLOAT128
B = np.uint8
UINT = unsignedinteger
UINT4 = np.uint8
UINT8 = np.uint8
UINT16 = np.uint16
UINT24 = np.uint32
UINT32 = np.uint32
FLOAT = float
BFLOAT16 = np.float16
FLOAT16 = np.float16
FLOAT32 = np.float32
FLOAT64 = np.float64
FLOAT128 = np.float64
param_dict = {"float128": [128, 15, 112, 16385], "float64": [64, 11, 52, 1025], "float32": [32, 8, 23, 129], "float16": [16, 5, 10, 17], "bfloat16": [16, 8, 7, 129]}

def separate4(a: str) -> Tuple[B, B, B, B]:
    # separate str to 4bit binary
    return B(a[0]), B(a[1]), B(a[2]), B(a[3])

def separate8(a: str) -> Tuple[B, B, B, B, B, B, B, B]:
    # separate str to 8bit binary
    return B(a[0]), B(a[1]), B(a[2]), B(a[3]), B(a[4]), B(a[5]), B(a[6]), B(a[7])

def separate16(a: str) -> Tuple[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]:
    # separate str to 16bit binary
    return B(a[0]), B(a[1]), B(a[2]), B(a[3]), B(a[4]), B(a[5]), B(a[6]), B(a[7]),\
          B(a[8]), B(a[9]), B(a[10]), B(a[11]), B(a[12]), B(a[13]), B(a[14]), B(a[15])

def concat4(a: Tuple[B, B, B, B]) -> str:
    # concat 4bit binary to str
    return str(a[0]) + str(a[1]) + str(a[2]) + str(a[3])

def concat5(a: Tuple[B, B, B, B, B]) -> str:
    # concat 5bit binary to str
    return str(a[0]) + str(a[1]) + str(a[2]) + str(a[3]) + str(a[4])

def concat8(a: Tuple[B, B, B, B, B, B, B, B]) -> str:
    # concat 8bit binary to str
    return str(a[0]) + str(a[1]) + str(a[2]) + str(a[3]) + str(a[4]) + str(a[5]) + str(a[6]) + str(a[7])

def concat9(a: Tuple[B, B, B, B, B, B, B, B, B]) -> str:
    # concat 9bit binary to str
    return str(a[0]) + str(a[1]) + str(a[2]) + str(a[3]) + str(a[4]) + str(a[5]) + str(a[6]) + str(a[7]) +\
          str(a[8])

def concat16(a: Tuple[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]) -> str:
    # concat 16bit binary to str
    return str(a[0]) + str(a[1]) + str(a[2]) + str(a[3]) + str(a[4]) + str(a[5]) + str(a[6]) + str(a[7]) +\
          str(a[8]) + str(a[9]) + str(a[10]) + str(a[11]) + str(a[12]) + str(a[13]) + str(a[14]) + str(a[15])

def d_to_bin(a: UINT, nbit: UINT) -> str:
    # decimal to binary
    b = bin(a)[2:]
    while len(b) < nbit:
        b = '0' + b
    return b

def bin_to_d(a: str) -> int:
    # binary to decimal
    return int(a, 2)

def d_to_fp(a: FLOAT, fp_type: str) -> str: #genrerated by chatGPT
    # decimal to floating point
    len_fp = param_dict[fp_type][0]
    len_exp = param_dict[fp_type][1]
    len_frac = param_dict[fp_type][2]
    offset = 2**(len_exp -1) -1
    if np.isnan(a):
        raise ValueError("NaN is not supported")
    elif np.isposinf(a):
        return '0' + '1' * len_exp + '0' * len_frac
    elif np.isneginf(a):
        return '1' + '1' * len_exp + '0' * len_frac
    elif a == 0:
        return '0' * len_fp
    else:
        # Check if the number is positive or negative
        sign_bit = '0' if a >= 0 else '1'
        a = abs(a)
        # Separate the integer and fractional parts of the number
        integer_part = int(a)
        fractional_part = a - integer_part
        # Convert the integer part to binary
        integer_binary = bin(integer_part)[2:]
        # Convert the fractional part to binary
        fractional_binary = ''
        while fractional_part != 0:
            fractional_part *= 2
            bit = int(fractional_part)
            fractional_binary += str(bit)
            fractional_part -= bit
        # Combine the integer and fractional parts
        binary = integer_binary + '.' + fractional_binary
        # Normalize the binary representation
        exponent = 0
        if '.' in binary:
            index = binary.index('.')
            if index != 0:
                binary = binary[index-1:index] + binary[:index-1] + binary[index+1:]
                exponent = index - 1
            else:
                while binary[0] != '1':
                    binary = binary[1:] + '0'
                    exponent -= 1
        # Calculate the biased exponent
        biased_exponent = exponent + offset
        # Convert the biased exponent to binary
        exponent_binary = format(biased_exponent, f'0{len_exp}b')
        # Convert the binary significand
        significand_binary = integer_binary[1:] + fractional_binary
        # Pad with zeros if necessary
        significand_binary = significand_binary.ljust(len_frac, '0')

        return sign_bit + exponent_binary + significand_binary


def decode_fp(a: str, fp_type: str) -> Tuple[str, str, str]:
    # decode floating point to sign, exponent, fraction
    len_fp = param_dict[fp_type][0]
    len_exp = param_dict[fp_type][1]
    if len(a) != len_fp:
        raise ValueError("Error: input bianry required " + str(len_fp) + "bit")
    return a[0], a[1:len_exp +1], a[len_exp +1:]

def b_to_fp(binary: str, fp_type: str) -> Tuple[Tuple[str, str], Tuple[int, int, FLOAT], FLOAT]:
        # binary to floating point
        len_fp = param_dict[fp_type][0]
        len_exp = param_dict[fp_type][1]
        len_frac = param_dict[fp_type][2]
        offset = 2**(len_exp -1) -1
        if len(binary) != len_fp:
            raise ValueError("Error: input bianry required " + str(len_fp) + "bit")
        
        sign = 1 if binary[0] == '0' else -1
        exponent = bin_to_d(binary[1:len_exp +1]) - offset
        fraction = bin_to_d(binary[len_exp +1:])/(2**(len_frac))

        if bin_to_d(binary[1:len_exp]) == 0:
            if bin_to_d(binary[len_exp:]) == 0:
                if binary[0] == '0':
                    ans = 0
                else:
                    ans = -0
            else:
                ans = sign * fraction * 2**(-offset +1)
        elif bin_to_d(binary[1:len_exp +1]) == 2**len_exp -1:
            if bin_to_d(binary[len_exp +1:]) == 0:
                if binary[0] == '0':
                    ans = np.inf
                else:
                    ans = -np.inf
            else:
                ans = np.nan
        else:
            ans = sign * (1 + fraction) * (2**exponent)
            
        return [fp_type, binary], [sign, exponent, fraction], ans

# def d_to_hex(a: np.uint8) -> str:
#     # decimal to hex
#     return hex(a)

# def hex_to_(a: str) -> np.uint8:
#     # hex to decimal
#     return np.uint8(int(a, 16))