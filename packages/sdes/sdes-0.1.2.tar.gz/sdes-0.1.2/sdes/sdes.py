from bitarray import bitarray

# Permutation function
def permute(bits, table):
    return bitarray([bits[i - 1] for i in table])

# Left shift function
def shift_left(bits, n):
    return bits[n:] + bits[:n]

# XOR function
def xor(bits1, bits2):
    return bits1 ^ bits2  # bitarray supports XOR directly

# S-Box Lookup
SBOXES = [
    [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]],
    [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
]

def s_box(bits, sbox):
    row, col = int(f"{bits[0]}{bits[3]}", 2), int(f"{bits[1]}{bits[2]}", 2)
    return bitarray(format(SBOXES[sbox][row][col], "02b"))

# Generate two subkeys from a 10-bit key
def generate_keys(key):
    P10, P8 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6], [6, 3, 7, 4, 8, 5, 10, 9]
    key = permute(key, P10)
    L, R = shift_left(key[:5], 1), shift_left(key[5:], 1)
    key1 = permute(L + R, P8)
    L, R = shift_left(L, 2), shift_left(R, 2)
    key2 = permute(L + R, P8)
    return key1, key2

# S-DES F-Function
def f_function(bits, key):
    EP, P4 = [4, 1, 2, 3, 2, 3, 4, 1], [2, 4, 3, 1]
    R_expanded = permute(bits[4:], EP)
    xor_result = xor(R_expanded, key)
    sbox_output = s_box(xor_result[:4], 0) + s_box(xor_result[4:], 1)
    return xor(bits[:4], permute(sbox_output, P4)) + bits[4:]

# Encrypt function
def encrypt(plaintext, key1, key2):
    IP, IP_inv = [2, 6, 3, 1, 4, 8, 5, 7], [4, 1, 3, 5, 7, 2, 8, 6]
    bits = permute(plaintext, IP)
    bits = f_function(bits, key1)
    bits = bits[4:] + bits[:4]  # Swap
    bits = f_function(bits, key2)
    return permute(bits, IP_inv)

# Decrypt function (just swap keys)
def decrypt(ciphertext, key1, key2):
    return encrypt(ciphertext, key2, key1)

