#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
#

import getopt
import sys
import math

KEY_LENGTH = 64


def prepare():
    with open('orig.txt') as orig, open('plain.txt', 'w') as plain:
        line_counter = 0
        for ch in orig.read().replace('\n', ''):
            plain.write(ch)
            line_counter += 1
            if (line_counter % KEY_LENGTH == 0):
                plain.write('\n')


def encrypt():
    pass


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
