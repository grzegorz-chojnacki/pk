#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
#

import getopt
import sys
import math
from itertools import combinations

KEY_LENGTH = 64

File = {
    'orig':    'orig.txt',
    'plain':   'plain.txt',
    'crypto':  'crypto.txt',
    'decrypt': 'decrypt.txt',
    'key':     'key.txt',
}

ZERO = '\x00'


def prepare():
    with open(File['orig']) as orig, open(File['plain'], 'w') as plain:
        written = 0
        for ch in orig.read().replace('\n', ''):
            plain.write(ch)
            written += 1
            if (written % KEY_LENGTH == 0):
                plain.write('\n')


def encrypt():
    with (open(File['plain']) as plain,
          open(File['key']) as key,
          open(File['crypto'], 'w') as crypto):
        key = key.readline().strip()
        assert len(key) == KEY_LENGTH
        for line in plain.readlines():
            # Strip '\n' and pad with spaces to KEY_LENGTH
            line = line[:-1].ljust(KEY_LENGTH)
            assert len(line) == KEY_LENGTH
            crypto.write(xor(line, key))


def xor(line, key):
    crypto = [ord(l) ^ ord(k) for l, k in zip(line, key)]
    return ''.join(map(chr, crypto))


def crack(bytes):
    spaces = set()
    for pair in space_pairs(bytes):
        if len(spaces) != 0:
            space = spaces.intersection(pair).pop()
            return chr(space ^ ord(' '))
        spaces = spaces.union(pair)
    return ZERO


def space_pairs(bytes):
    return filter(is_space_pair, combinations(set(bytes), 2))


def is_space_pair(pair):
    b1, b2 = pair
    return 0b_010_00000 < b1 ^ b2 < 0b_010_111111


def analyse():
    with (open(File['crypto'], 'rb') as crypto,
          open(File['decrypt'], 'w') as decrypt):
        crypto = list(chunks(crypto.read(), KEY_LENGTH))
        assert len(crypto[-1]) == KEY_LENGTH
        key = ''.join(crack(column) for column in zip(*crypto))

        for line in to_text(crypto):
            decrypt.write(xor(line, key) + '\n')

        return key


def chunks(text, n):
    for i in range(0, len(text), n):
        yield text[i:i + n]


def to_text(bytes):
    return map(lambda line: map(chr, line), bytes)


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'pek')
        for o, _ in opts:
            if o == '-p':
                prepare()
                print('Zakończono przygotowywanie')
            elif o == '-e':
                encrypt()
                print('Zakończono szyfrowanie')
            elif o == '-k':
                key = analyse()
                key_type = 'częściowy' if ZERO in key else 'pełny'
                print(f'Znaleziono {key_type} klucz: "{key.replace(ZERO, "_")}"')
                print('Zakończono odszyfrowywanie')

    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: \"{err.filename}\"')
        sys.exit(3)


if __name__ == "__main__":
    main()
