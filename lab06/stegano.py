#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import getopt
import sys
import itertools as it


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


def line_end_space_encrypt(bits):
    with open('cover.html') as src, open('watermark.html', 'w') as dst:
        lines = [line[:-1] + ' \n' if bit == '1' else line
                 for (bit, line) in it.zip_longest(bits, src.readlines())]
        dst.writelines(lines)


def line_end_space_decrypt():
    with open('watermark.html') as src, open('detect.txt', 'w') as dst:
        bits = ['1' if len(line) >= 2 and line[-2] == ' ' else '0'
                for line in src.readlines()]

        dst.writelines(decrypt(bits))


def single_double_space_encrypt(bits):
    pass


def single_double_space_decrypt():
    pass


def fake_typo_insertion_encrypt(bits):
    pass


def fake_typo_insertion_decrypt():
    pass


def useless_tag_insertion_encrypt(bits):
    pass


def useless_tag_insertion_decrypt():
    pass


def main():
    try:
        # opts, _ = getopt.getopt(sys.argv[1:], 'de1234')
        # operation = encryption = None

        # for o, _ in opts:
        #     if o == '-e':
        #         encryption = True
        #     elif o == '-d':
        #         encryption = False

        # for o, _ in opts:
        #     if o == '-1':
        #         operation = line_end_space_encrypt if encryption else line_end_space_decrypt
        #     elif o == '-2':
        #         operation = single_double_space_encrypt if encryption else single_double_space_decrypt
        #     elif o == '-3':
        #         operation = fake_typo_insertion_encrypt if encryption else fake_typo_insertion_decrypt
        #     elif o == '-4':
        #         operation = useless_tag_insertion_encrypt if encryption else useless_tag_insertion_decrypt

        # if operation is None or encryption is None:
        #     raise getopt.GetoptError('')

        with open('mess.txt') as mess:
            msg = mess.read()
            line_end_space_encrypt(encrypt(msg))
            line_end_space_decrypt()

    except getopt.GetoptError:
        print(f'użycie: {sys.argv[0]} -[de] -[1234]')
        sys.exit(1)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(2)


if __name__ == "__main__":
    main()
