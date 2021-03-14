#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
#

import getopt
import sys
import math
import itertools as it

KEY_LENGTH = 64

File = {
    'orig':    'orig.txt',
    'plain':   'plain.txt',
    'crypto':  'crypto.txt',
    'decrypt': 'decrypt.txt',
    'key':     'key.txt',
}

ZERO = '\x00'


def chunks(text, n):
    for i in range(0, len(text), n):
        yield text[i:i + n]


def prepare():
    with open(File['orig']) as orig, open(File['plain'], 'w') as plain:
        line_counter = 0
        for ch in orig.read().replace('\n', ''):
            plain.write(ch)
            line_counter += 1
            if (line_counter % KEY_LENGTH == 0):
                plain.write('\n')


def xor(line, key):
    crypto = [ord(l) ^ ord(k) for l, k in zip(line, key)]
    return ''.join(map(chr, crypto))


def encrypt():
    with (open(File['plain']) as plain,
          open(File['key']) as key,
          open(File['crypto'], 'w') as crypto):
        key = key.readline().strip()
        assert len(key) == KEY_LENGTH
        for line in plain.readlines():
            line = line[:-1].ljust(KEY_LENGTH)
            assert len(line) == KEY_LENGTH
            crypto.write(xor(line, key))


def maybe_space(b1, b2):
    return 0b010_00000 < b1 ^ b2 < 0b010_111111


def crack(bytes):
    spaces = set()
    for pair in it.combinations(set(bytes), 2):
        if maybe_space(*pair):
            if len(spaces) > 0:
                space = spaces.intersection(pair).pop()
                return chr(space ^ ord(' '))
            else:
                spaces = spaces.union(pair)
    else:
        return ZERO


def analyse():
    with (open(File['crypto'], 'rb') as crypto,
          open(File['decrypt'], 'w') as decrypt):
        crypto = list(chunks(crypto.read(), KEY_LENGTH))
        assert len(crypto[-1]) == KEY_LENGTH
        key = ''.join(crack(column) for column in zip(*crypto))

        if ZERO not in key:
            print('Znaleziono pełny klucz:')
        else:
            print('Znaleziono niepełny klucz:')
        print(key.replace(ZERO, '_'))

        for line in map(lambda line: map(chr, line), crypto):
            decrypt.write(xor(line, key) + '\n')


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'pek')
        for o, _ in opts:
            if o == '-p':
                prepare()
            elif o == '-e':
                encrypt()
            elif o == '-k':
                analyse()

    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: \"{err.filename}\"')
        sys.exit(3)


if __name__ == "__main__":
    main()
