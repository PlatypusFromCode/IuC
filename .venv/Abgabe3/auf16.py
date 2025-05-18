from itertools import product
from scipy.spatial.distance import hamming
import numpy as np


codewords = [
    "00000000", "00001111", "00110011", "00111100", "01010101",
    "01011010", "01100110", "01101001", "11111111", "11110000",
    "11001100", "11000011", "10100101", "10011001", "10010110"
]


code_arr = np.array([[int(bit) for bit in cw] for cw in codewords])


def hamming_distance(a, b):
    return np.sum(a != b)


min_d = 8
for i in range(len(code_arr)):
    for j in range(i + 1, len(code_arr)):
        dist = hamming_distance(code_arr[i], code_arr[j])
        if dist < min_d:
            min_d = dist


all_words = list(product([0, 1], repeat=8))
existing_set = set(tuple(row) for row in code_arr)


c16 = None
for word in all_words:
    if word in existing_set:
        continue
    if all(hamming_distance(np.array(word), cw) >= min_d for cw in code_arr):
        c16 = word
        break

c16_str = ''.join(map(str, c16)) if c16 else None
min_d, c16_str

print(c16_str)