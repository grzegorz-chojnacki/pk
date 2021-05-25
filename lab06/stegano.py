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


def encrypt_regex(msg, regex, replace_fn):
    with open('cover.html') as src, open('watermark.html', 'w') as dst:
        bits = iter(encrypt(msg))
        data = re.sub(regex, replace_fn(bits), src.read())

        assert next(bits, None) is None

        dst.write(data)


def decrypt_regex(regex, find_fn):
    with open('watermark.html') as src, open('detect.txt', 'w') as dst:
        found = re.findall(regex, src.read())
        bits = find_fn(found)
        dst.write(decrypt(bits))


def line_end_space_encrypt(bits):
    def sub(m):
        if next(bits, None) == '1':
            return ' \n'
        else:
            return '\n'
    return sub


def line_end_space_decrypt(found):
    bits = []
    for maybe_space in found:
        if maybe_space == ' ':
            bits.append('1')
        else:
            bits.append('0')
    return bits


def single_double_space_encrypt(bits):
    def sub(m):
        if next(bits, None) == '1':
            return '  '
        else:
            return ' '
    return sub


def single_double_space_decrypt(found):
    bits = []
    for maybe_space in found:
        if maybe_space != '':
            bits.append('1')
        else:
            bits.append('0')
    return bits


def fake_typo_insertion_encrypt(bits):
    pass


def fake_typo_insertion_decrypt():
    pass


def useless_tag_insertion_encrypt(bits):
    def sub(m):
        tag = m.group(1)
        attrs = m.group(2) or ''
        if next(bits, None) == '1':
            return f'<{tag} style="display: none"></{tag}><{tag}{attrs}>'
        else:
            return f'<{tag}{attrs}>'
    return sub


def useless_tag_insertion_decrypt(found):
    bits = []
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
    return bits


algorithms = {
    "line_end": {
        "encrypt": line_end_space_encrypt,
        "decrypt": line_end_space_decrypt,
        "regex": r'( )?\n',
    },
    "double_space": {
        "encrypt": single_double_space_encrypt,
        "decrypt": single_double_space_decrypt,
        "regex": r' ( )*',
    },
    "fake_typo": {
        "encrypt": fake_typo_insertion_encrypt,
        "decrypt": fake_typo_insertion_decrypt,
        "regex": None,
    },
    "useless_tag": {
        "encrypt": useless_tag_insertion_encrypt,
        "decrypt": useless_tag_insertion_decrypt,
        "regex": r'<(div|p|li|td)( [^\\]*?)?>',
    },
}


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'de1234')
        algorithm_key = encryption = None

        for o, _ in opts:
            if o == '-e':
                encryption = True
            elif o == '-d':
                encryption = False

        for o, _ in opts:
            if o == '-1':
                algorithm_key = "line_end"
            elif o == '-2':
                algorithm_key = "double_space"
            elif o == '-3':
                algorithm_key = "fake_typo"
            elif o == '-4':
                algorithm_key = "useless_tag"

        if algorithm_key is None or encryption is None:
            raise getopt.GetoptError('')

        algorithm = algorithms[algorithm_key]

        if encryption:
            with open('mess.txt') as mess:
                msg = mess.read()
                encrypt_regex(msg, algorithm["regex"], algorithm["encrypt"])
        else:
            decrypt_regex(algorithm["regex"], algorithm["decrypt"])

    except getopt.GetoptError:
        print(f'użycie: {sys.argv[0]} -[de] -[1234]')
        sys.exit(1)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(2)
    except AssertionError:
        print(f'Podana wiadomość jest za długa')
        sys.exit(3)


if __name__ == "__main__":
    main()
