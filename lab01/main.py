#!/usr/bin/env python3
import getopt
import sys
import math
import caesar
import affine
from common import File


def transform(method, input_file, output_file):
    with open(File[input_file]) as text, open(File['key']) as key, open(File[output_file], 'w') as output:
        key_str = next(key)
        result = ''.join([method(letter, key_str)
                          for letter in text.read()])
        output.write(result)
        return True


def encrypt(algorithm):
    if transform(algorithm.encrypt, 'plain', 'crypto'):
        print('Poprawnie zaszyfrowano')


def decrypt(algorithm):
    if transform(algorithm.decrypt, 'crypto', 'decrypt'):
        print('Poprawnie odszyfrowano')


def brute_force(algorithm):
    with open(File['crypto']) as crypto, open(File['decrypt'], 'w') as output:
        crypto = crypto.read()
        for key in algorithm.key_range():
            result = ''.join([algorithm.decrypt(letter, key)
                              for letter in crypto])
            output.write(f'### Key: {key}\n')
            output.write(result)
            output.write('\n')
        print('Zakończono odszyfrowywanie')


def find_key(algorithm):
    with open(File['crypto']) as crypto, open(File['extra']) as extra, open(File['decrypt'], 'w') as output, open(File['key_found'], 'w') as key_found:
        crypto = crypto.read()
        extra = extra.read()
        keys = [algorithm.find_key(pair) for pair in zip(extra, crypto)]
        key = set.intersection(*keys).pop()
        key_found.write(key)
        result = ''.join([algorithm.decrypt(letter, key) for letter in crypto])
        output.write(result)
        print('Znaleziono pasujący klucz')


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'caedjk')
        operation = algorithm = None
        for o, _ in opts:
            if o == '-c':
                algorithm = caesar
            elif o == '-a':
                algorithm = affine
            elif o == '-e':
                operation = encrypt
            elif o == '-d':
                operation = decrypt
            elif o == '-j':
                operation = find_key
            elif o == '-k':
                operation = brute_force

        if operation is None or algorithm is None:
            print(f'użycie: {sys.argv[0]} -[ac] -[edjk]')
            sys.exit(2)
        else:
            try:
                operation(algorithm)
            except FileNotFoundError as err:
                print(f'Nie znaleziono pliku \"{err.filename}\"')
                sys.exit(3)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
