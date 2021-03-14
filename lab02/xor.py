#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
#

import getopt
import sys
import math
from itertools import combinations

KEY_LENGTH = 64
ZERO = '\x00'

File = {
    'orig':    'orig.txt',
    'plain':   'plain.txt',
    'crypto':  'crypto.txt',
    'decrypt': 'decrypt.txt',
    'key':     'key.txt',
}


def prepare():
    with open(File['orig']) as orig, open(File['plain'], 'w') as plain:
        written = 0
        for ch in orig.read().replace('\n', ''):
            plain.write(ch.lower())
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
            line = line.replace('\n', '').ljust(KEY_LENGTH)
            assert len(line) == KEY_LENGTH
            crypto.write(xor(line, key))


def xor(line, key):
    crypto = (chr(ord(l) ^ ord(k)) for l, k in zip(line, key))
    return ''.join(crypto)


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
        assert len(crypto[-1]) == KEY_LENGTH  # only last line can be shorter
        key = ''.join(crack(column) for column in zip(*crypto))

        for line in to_text(crypto):
            decrypt.write(printable_line(xor(line, key)))

        return key


def chunks(text, n):
    for i in range(0, len(text), n):
        yield text[i:i + n]


def to_text(bytes):
    return map(lambda line: map(chr, line), bytes)


def printable_line(line):
    cleaned = (c if c.isprintable() else '_' for c in line)
    return ''.join(cleaned) + '\n'


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'pek')
        if len(opts) != 1:
            raise getopt.GetoptError('')

        opt, _ = opts[0]
        if opt == '-p':
            prepare()
            print('Zakończono przygotowywanie')
        elif opt == '-e':
            encrypt()
            print('Zakończono szyfrowanie')
        elif opt == '-k':
            key = analyse()
            key_t = 'częściowy' if ZERO in key else 'pełny'
            print(f'Znaleziono {key_t} klucz: "{key.replace(ZERO, "_")}"')
            print('Zakończono odszyfrowywanie')
        else:
            raise getopt.GetoptError('')
    except getopt.GetoptError:
        print(f'użycie: {sys.argv[0]} -[ekp]')
        sys.exit(1)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(2)
    except AssertionError:
        print(f'Długość klucza/linii inna niż {KEY_LENGTH}')
        sys.exit(3)


if __name__ == "__main__":
    main()
