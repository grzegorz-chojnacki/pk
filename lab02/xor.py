#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import getopt
import sys
from itertools import combinations

TRANSLATION_TABLE = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')
ALLOWED_CHARACTERS = set(' abcdefghijklmnopqrstuvwxyz')
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
        text = orig.read().replace('\n', '').translate(TRANSLATION_TABLE).lower()
        written = 0
        for ch in text:
            if ch not in ALLOWED_CHARACTERS:
                raise SyntaxError(ch)
            plain.write(ch)
            written += 1
            if written % KEY_LENGTH == 0:
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


def crack(bytes):
    spaces = set()
    for pair in space_pairs(bytes):
        if len(spaces) > 0:
            space = spaces.intersection(pair).pop()
            return chr(space ^ ord(' '))
        spaces = set(pair)
    return ZERO


def space_pairs(bytes):
    return filter(is_space_pair, combinations(set(bytes), 2))


def is_space_pair(pair):
    b1, b2 = pair
    return 0b_010_00000 < b1 ^ b2 < 0b_010_111111


def to_text(bytes):
    return map(lambda line: map(chr, line), bytes)


def printable_line(line):
    return ''.join(c if c.isprintable() else '_' for c in line) + '\n'


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
            print(f'Znaleziono klucz: "{key.replace(ZERO, "_")}"')
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
    except SyntaxError as err:
        print(f'W pliku występuje niedozwolony symbol: "{err.args[0]}"')
        sys.exit(4)


if __name__ == "__main__":
    main()
