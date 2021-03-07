#!/usr/bin/env python3
import getopt
import sys
import math

File = {
    'plain':     'plain.txt',
    'crypto':    'crypto.txt',
    'decrypt':   'decrypt.txt',
    'key':       'key.txt',
    'extra':     'extra.txt',
    'key_found': 'key-found.txt',
}

ALPHABET_SIZE = 26


def case_offset(letter):
    if letter.isupper():
        return ord('A')
    else:
        return ord('a')


class Caesar:
    @staticmethod
    def key_range():
        return range(1, ALPHABET_SIZE)

    @staticmethod
    def parse_key(key_str):
        try:
            key = int(key_str)
            if key not in Caesar.key_range():
                raise Exception()
            else:
                return key
        except:
            print(f'Zły format klucza: {key_str}')
            sys.exit(3)

    @staticmethod
    def encrypt(letter, key_str):
        key = Caesar.parse_key(key_str)
        if letter.isalpha():
            offset = case_offset(letter)
            return chr((ord(letter) - offset + key) % ALPHABET_SIZE + offset)
        else:
            return letter

    @staticmethod
    def decrypt(letter, key_str):
        key = Caesar.parse_key(key_str)
        if letter.isalpha():
            offset = case_offset(letter)
            return chr((ord(letter) - offset - key) % ALPHABET_SIZE + offset)
        else:
            return letter

    @staticmethod
    def find_key(pair):
        e, c = pair
        result = set()
        for key in Caesar.key_range():
            if Caesar.encrypt(e, key) == c:
                result.add(str(key))
        return result

class Affine:
    @staticmethod
    def key_range():
        return [f'{a} {b}' # ToDo: zmienić miejsce parsowania klucza, tak by można było zwrócić tu krotke
                for a in range(1, ALPHABET_SIZE) if math.gcd(a, ALPHABET_SIZE) == 1
                for b in range(0, ALPHABET_SIZE)
                ]

    @staticmethod
    def parse_key(key_str):
        try:
            a, b = key_str.split()
            a = Caesar.parse_key(a)
            b = int(b)
            if math.gcd(a, ALPHABET_SIZE) == 1:
                return a, b
            else:
                raise Exception()
        except:
            print(f'Zły format klucza: {key_str}')
            sys.exit(3)

    @staticmethod
    def encrypt(letter, key_str):
        a, b = Affine.parse_key(key_str)
        if letter.isalpha():
            offset = case_offset(letter)
            return chr((a * (ord(letter) - offset) + b) % ALPHABET_SIZE + offset)
        else:
            return letter

    @staticmethod
    def decrypt(letter, key_str):
        a, b = Affine.parse_key(key_str)
        a = pow(a, -1, ALPHABET_SIZE)
        if letter.isalpha():
            offset = case_offset(letter)
            return chr(a * (ord(letter) - offset - b) % ALPHABET_SIZE + offset)
        else:
            return letter

    @staticmethod
    def find_key(pair):
        e, c = pair
        result = set()
        for key in Affine.key_range():
            if Affine.encrypt(e, key) == c:
                result.add(key)
        return result


def transform(method, input_file, output_file):
    with open(File[input_file]) as text, open(File['key']) as key, open(File[output_file], 'w') as output:
        try:
            key_str = next(key)
            result = ''.join([method(letter, key_str)
                              for letter in text.read()])
            output.write(result)
            return True
        except FileNotFoundError as err:
            print(f'Nie znaleziono pliku \"{err.filename}\"')
            sys.exit(2)


def encrypt(algorithm):
    if transform(algorithm.encrypt, 'plain', 'crypto'):
        print('Poprawnie zaszyfrowano')


def decrypt(algorithm):
    if transform(algorithm.decrypt, 'crypto', 'decrypt'):
        print('Poprawnie odszyfrowano')


def brute_force(algorithm):
    with open(File['crypto']) as crypto, open(File['decrypt'], 'w') as output:
        crypto = crypto.read()
        try:
            for key in algorithm.key_range():
                result = ''.join([algorithm.decrypt(letter, key)
                                  for letter in crypto])
                output.write(f'### Key: {key}\n')
                output.write(result)
                output.write('\n')
            print('Zakończono odszyfrowywanie')
        except FileNotFoundError as err:
            print(f'Nie znaleziono pliku \"{err.filename}\"')
            sys.exit(2)

def find_key(algorithm):
    with open(File['crypto']) as crypto, open(File['extra']) as extra, open(File['decrypt'], 'w') as output, open(File['key_found'], 'w') as key_found:
        crypto = crypto.read()
        extra  = extra.read()
        try:
            keys = [algorithm.find_key(pair) for pair in zip(extra, crypto)]
            key = set.intersection(*keys).pop()
            key_found.write(key)
            result = ''.join([algorithm.decrypt(letter, key) for letter in crypto])
            output.write(result)
        except FileNotFoundError as err:
            print(f'Nie znaleziono pliku \"{err.filename}\"')
            sys.exit(2)


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'caedjk')
        operation = algorithm = None
        for o, _ in opts:
            if o == '-c':
                algorithm = Caesar
            elif o == '-a':
                algorithm = Affine
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
            operation(algorithm)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
