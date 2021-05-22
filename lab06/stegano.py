#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import getopt
import sys
from math import gcd
from random import randint


def line_end_space(msg):
    pass


def single_double_space(msg):
    pass


def fake_typo_insertion(msg):
    pass


def useless_tag_insertion(msg):
    pass


def encrypt(msg):
    def transform(c):
        binary = bin(int(c, 16))[2:]
        padded = binary.rjust(4, '0')
        return list(padded)

    return sum(list(map(transform, msg)), [])


def chunks(array, n):
    for i in range(0, len(array), n):
        yield array[i:i + n]

def decrypt(bits):
    def transform(bits):
        binary = int(''.join(bits), 2)
        return hex(binary)[2:]

    return ''.join(map(transform, chunks(bits, 4)))


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'de1234')
        operation = method = None

        for o, _ in opts:
            if o == '-e':
                method = encrypt
            elif o == '-d':
                method = decrypt
            elif o == '-1':
                operation = line_end_space
            elif o == '-2':
                operation = single_double_space
            elif o == '-3':
                operation = fake_typo_insertion
            elif o == '-4':
                operation = useless_tag_insertion

        if operation is None or method is None:
            raise getopt.GetoptError('')
        else:
            with open('mess.txt') as mess:
                msg = mess.read()
                print(decrypt(encrypt(msg)))


    except getopt.GetoptError:
        print(f'użycie: {sys.argv[0]} -[de] -[1234]')
        sys.exit(1)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(2)


if __name__ == "__main__":
    main()
