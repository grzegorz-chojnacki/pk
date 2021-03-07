import math
import caesar
from common import ALPHABET_SIZE, case_offset


def key_range():
    return [(a, b)
            for a in range(1, ALPHABET_SIZE) if math.gcd(a, ALPHABET_SIZE) == 1
            for b in range(0, ALPHABET_SIZE)
            ]


def parse_key(key_str):
    a, b = key_str.split()
    a = caesar.parse_key(a)
    b = int(b)
    assert math.gcd(a, ALPHABET_SIZE) == 1, key_str
    return a, b


def encrypt(letter, key):
    a, b = key
    if letter.isalpha():
        offset = case_offset(letter)
        return chr((a * (ord(letter) - offset) + b) % ALPHABET_SIZE + offset)
    else:
        return letter


def decrypt(letter, key):
    a, b = key
    a = pow(a, -1, ALPHABET_SIZE)
    if letter.isalpha():
        offset = case_offset(letter)
        return chr(a * (ord(letter) - offset - b) % ALPHABET_SIZE + offset)
    else:
        return letter


def find_key(pair):
    e, c = pair
    result = set()
    for key in key_range():
        if encrypt(e, key) == c:
            result.add(key)
    return result

def key_str(key):
    a, b = key
    return f'{a} {b}'
