#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
#

import getopt
import sys
import math

KEY_LENGTH = 64

File = {
    'orig':    'orig.txt',
    'plain':   'plain.txt',
    'crypto':  'crypto.txt',
    'decrypt': 'decrypt.txt',
    'key':     'key.txt',
}


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
            line = line.strip().ljust(KEY_LENGTH)
            assert len(line) == KEY_LENGTH
            crypto.write(xor(line, key))


def analyse():
    pass


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
