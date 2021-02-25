#!/usr/bin/env python3
import getopt, sys

File = {
    'plain':     'plain.txt',
    'crypto':    'crypto.txt',
    'decrypt':   'decrypt.txt',
    'key':       'key.txt',
    'extra':     'extra.txt',
    'key_found': 'key-found.txt',
}

def caseOffset(letter):
    if letter.isupper():
        return ord('A')
    else:
        return ord('a')

class Caesar:
    @staticmethod
    def encrypt(letter, key):
        if letter.isalpha():
            offset = caseOffset(letter)
            return chr((ord(letter) - offset + key) % 26 + offset)
        else:
            return letter

    @staticmethod
    def decrypt(letter, key):
        if letter.isalpha():
            offset = caseOffset(letter)
            return chr((ord(letter) - offset - key) % 26 + offset)
        else:
            return letter


def afinic():
    pass

def transform(method, input_file, output_file):
    with open(File[input_file]) as text, open(File['key']) as key:
        try:
            key = int(next(key))
            if key not in range(1, 26):
                raise Exception()
            output = open(File[output_file], 'w')
            result = ''.join([ method(letter, key) for letter in text.read() ])
            output.write(result)
            output.close()
            return True
        except FileNotFoundError as err:
            print('Nie znaleziono pliku ' + err.filename)
        except:
            print('Klucz nie jest liczbą z zakresu: 1..25')
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
    if   o == '-c':
        algorithm = Caesar
    elif o == '-a':
        algorithm = afinic
    elif o == '-e':
        operation = encrypt
    elif o == '-d':
        operation = decrypt
    elif o == '-j':
        pass
    elif o == '-k':
        pass

if operation is None or algorithm is None:
    print('usage: ' + sys.argv[0] +  ' -[ac] -[edjk]')
    sys.exit(2)

operation(algorithm)
