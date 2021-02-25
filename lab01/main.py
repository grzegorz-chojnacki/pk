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


def case_offset(letter):
    if letter.isupper():
        return ord('A')
    else:
        return ord('a')


class Caesar:
    @staticmethod
    def parseKey(key_str):
        try:
            key = int(key_str)
            if key not in range(1, 26):
                raise Exception()
            else:
                return key
        except:
            print(f'Zły format klucza: {key_str}')
            sys.exit(3)

    @staticmethod
    def encrypt(letter, key_str):
        key = Caesar.parseKey(key_str)
        if letter.isalpha():
            offset = case_offset(letter)
            return chr((ord(letter) - offset + key) % 26 + offset)
        else:
            return letter

    @staticmethod
    def decrypt(letter, key_str):
        key = Caesar.parseKey(key_str)
        if letter.isalpha():
            offset = case_offset(letter)
            return chr((ord(letter) - offset - key) % 26 + offset)
        else:
            return letter


class Afinic:
    @staticmethod
    def parseKey(key_str):
        try:
            a, b = key_str.split()
            a = Caesar.parseKey(a)
            b = int(b)
            if math.gcd(a, 26) == 1:
                return a, b
            else:
                raise Exception()
        except:
            print(f'Zły format klucza: {key_str}')
            sys.exit(3)

    @staticmethod
    def encrypt(letter, key_str):
        a, b = Afinic.parseKey(key_str)
        if letter.isalpha():
            offset = case_offset(letter)
            return chr((a * (ord(letter) - offset) + b) % 26 + offset)
        else:
            return letter

    @staticmethod
    def decrypt(letter, key_str):
        a, b = Afinic.parseKey(key_str)
        a = pow(a, -1, 26)
        if letter.isalpha():
            offset = case_offset(letter)
            return chr(a * (ord(letter) - offset - b) % 26 + offset)
        else:
            return letter


def transform(method, input_file, output_file):
    with open(File[input_file]) as text, open(File['key']) as key:
        try:
            output = open(File[output_file], 'w')
            key_str = next(key)
            result = ''.join([method(letter, key_str)
                              for letter in text.read()])
            output.write(result)
            output.close()
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


try:
    opts, args = getopt.getopt(sys.argv[1:], 'caedjk')
except getopt.GetoptError as err:
    print(err)
    sys.exit(1)

operation = None
algorithm = None

for o, a in opts:
    if o == '-c':
        algorithm = Caesar
    elif o == '-a':
        algorithm = Afinic
    elif o == '-e':
        operation = encrypt
    elif o == '-d':
        operation = decrypt
    elif o == '-j':
        pass
    elif o == '-k':
        pass

if operation is None or algorithm is None:
    print(f'usage: {sys.argv[0]} -[ac] -[edjk]')
    sys.exit(2)

operation(algorithm)
