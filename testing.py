""" Checksum Implementation """
SIZE = 8 # number of data blocks

def calculate_checksum(data):
    total = sum(data)
    while total > 255: # Handle wrap around (carry) - assuming 8-bit blocks
        total = (total & 255) + (total >> 8)

    checksum = ~total & 0xFF # 1's complement of the sum
    return checksum

def print_data(data):
    print(" ".join(str(d) for d in data))

def main():
    data = [25, 62, 3, 47, 200, 12, 89, 5]
    print_data(data)

    checksum = calculate_checksum(data)

    received_data = list(data) # Copy data to simulate "received" data

    pos = int(input(f"Enter position to corrupt: "))
    val = int(input(f"Enter new value: "))
    if 0 <= pos < SIZE:
        received_data[pos] = val

    print_data(received_data)

    total = 0
    for value in received_data:
        total += value
        if total > 255:
            total = (total & 255) + (total >> 8)
    total += checksum
    if total > 255:
        total = (total & 255) + (total >> 8)

    if total == 255:
        print("No error.")
    else:
        print("Error.")

""" Cyclic Redundancy Check """

def modulo2_division(augmented_data, key_len):
    """Perform Modulo2 (XOR) division and return the remainder string"""
    temp = list(augmented_data)
    length = len(temp)
    for i in range(0, length - key_len + 1):
        if temp[i] == "1":
            for j in range(key_len):
                temp[i + j] = "0" if temp[i + j] == key[j] else "1"

    remainder = "".join(temp[length - (key_len - 1):])
    return remainder

def generate_crc(data, key):
    """Sender side: Generate CRC and appends it to data to form codeword"""
    zeros_to_append = len(key) - 1
    augmented_data = data + ("0" * zeros_to_append)
    remainder = modulo2_division(augmented_data, len(key))
    codeword = data + remainder
    return codeword

def check_crc(received, key):
    """Receiver's side: Checks recieved codeword for errors"""
    remainder = modulo2_division(received, len(key))
    return set(remainder) <= {"0"}

def main():
    global key
    data = input("Enter binary string: ")
    key = input ("Enter Generator Key: ")
    codeword = generate_crc(data, key)
    received = codeword
    pos = int(input("Enter position to flip: "))
    flipped = "1" if received[pos] == "1" else "0"
    received = received[:pos] + flipped + received[pos + 1:]

    if check_crc(received, key):
        print("No error")
    else:
        print("Error")


""" Hamming Code """

def calculate_parity_bits(m: int):
    r = 0
    while (2**r) < (m + r + 1):
        r += 1
    return r

def is_power_of_2(n):
    return (n & (n-1)) == 0

def generate_hamming_code(data, total_len, parity_bits):
    """Sender's side: Generate hamming code from data bits"""
    hamming = {}
    j = 0

    # Place data bits into their correct positions, skip powers of 2
    for i in range(1, total_len + 1):
        if is_power_of_2(i):
            hamming[i] = -1 # Placeholder
        else:
            hamming[i] = data[i]
            j += 1


def main():
    data_len = int(input("Enter the number of data bits: "))
    data = list(map(int, input().split()))
    parity_bits = calculate_parity_bits(data_len)
    total_len = data_len + parity_bits

    hamming = generate_hamming_code(data, total_len, parity_bits)