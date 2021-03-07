from common import ALPHABET_SIZE, case_offset


def key_range():
    return range(1, ALPHABET_SIZE)


def parse_key(key_str):
    key = int(key_str)
    assert key in key_range(), key_str
    return key


def encrypt(letter, key):
    if letter.isalpha():
        offset = case_offset(letter)
        return chr((ord(letter) - offset + key) % ALPHABET_SIZE + offset)
    else:
        return letter


def decrypt(letter, key):
    if letter.isalpha():
        offset = case_offset(letter)
        return chr((ord(letter) - offset - key) % ALPHABET_SIZE + offset)
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
    return f'{key}'
