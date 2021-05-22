#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import getopt
import sys
import itertools as it
import regex as re


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
        lines = [line.replace(' \n', '\n') for line in src.readlines()]
        lines = [line[:-1] + ' \n' if bit == '1' else line
                 for (bit, line) in it.zip_longest(bits, lines)]
        dst.writelines(lines)


def line_end_space_decrypt():
    with open('watermark.html') as src, open('detect.txt', 'w') as dst:
        bits = ['1' if len(line) >= 2 and line[-2] == ' ' else '0'
                for line in src.readlines()]

        dst.writelines(decrypt(bits))


def single_double_space_encrypt(bits):
    with open('cover.html') as src, open('watermark.html', 'w') as dst:
        characters = ''.join([re.sub(r'([ ]+)', ' ', line)
                              for line in src.readlines()])
        bits = iter(bits)
        for c in characters:
            if c != ' ':
                dst.write(c)
            elif next(bits, None) == '1':
                dst.write('  ')
            else:
                dst.write(' ')


def single_double_space_decrypt():
    with open('watermark.html') as src, open('detect.txt', 'w') as dst:
        space_before = False
        bits = []
        for c in src.read():
            if c == ' ':
                if space_before:
                    space_before = False
                    bits.append('1')
                else:
                    space_before = True
            else:
                if space_before:
                    space_before = False
                    bits.append('0')

        dst.writelines(decrypt(bits))


def fake_typo_insertion_encrypt(bits):
    pass


def fake_typo_insertion_decrypt():
    pass


REGEX = r'<(div|p|li|td)( [^\\]*?)?>'

def useless_tag_insertion_encrypt(bits):
    with open('cover.html') as src, open('watermark.html', 'w') as dst:
        bits = iter(bits)

        def sub(m):
            tag = m.group(1)
            attrs = m.group(2) or ''
            if next(bits, None) == '1':
                return f'<{tag} style="display: none"></{tag}><{tag}{attrs}>'
            else:
                return f'<{tag}{attrs}>'

        data = re.sub(REGEX, sub, src.read())
        dst.write(data)


def useless_tag_insertion_decrypt():
    with open('watermark.html') as src, open('detect.txt', 'w') as dst:
        bits = []
        found = re.findall(REGEX, src.read())

        tag_before = False
        for (_, attrs) in found:
            if attrs == ' style="display: none"':
                bits.append('1')
                tag_before = True
            else:
                if tag_before:
                    tag_before = False
                else:
                    bits.append('0')

        dst.write(decrypt(bits))


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
            useless_tag_insertion_encrypt(encrypt(msg))
            useless_tag_insertion_decrypt()

    except getopt.GetoptError:
        print(f'użycie: {sys.argv[0]} -[de] -[1234]')
        sys.exit(1)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(2)


if __name__ == "__main__":
    main()
