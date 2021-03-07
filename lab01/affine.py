import math
import caesar
from common import ALPHABET_SIZE, case_offset


def key_range():
    return [f'{a} {b}'  # ToDo: zmienić miejsce parsowania klucza, tak by można było zwrócić tu krotke
            for a in range(1, ALPHABET_SIZE) if math.gcd(a, ALPHABET_SIZE) == 1
            for b in range(0, ALPHABET_SIZE)
            ]


def parse_key(key_str):
    a, b = key_str.split()
    a = caesar.parse_key(a)
    b = int(b)
    if math.gcd(a, ALPHABET_SIZE) == 1:
        return a, b
    else:
        raise Exception()


def encrypt(letter, key_str):
    a, b = parse_key(key_str)
    if letter.isalpha():
        offset = case_offset(letter)
        return chr((a * (ord(letter) - offset) + b) % ALPHABET_SIZE + offset)
    else:
        return letter


def decrypt(letter, key_str):
    a, b = parse_key(key_str)
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
