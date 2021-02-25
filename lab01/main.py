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

def encrypt(method):
    with open(File['plain']) as text, open(File['key']) as key:
        try:
            key = int(next(key))
            if key not in range(1, 26):
                raise Exception()
            output = open(File['crypto'], 'w')
            result = ''.join([ method.encrypt(letter, key) for letter in text.read() ])
            output.write(result)
            output.close()
            print('Poprawnie zaszyfrowano')
        except FileNotFoundError as err:
            print('Nie znaleziono pliku ' + err.filename)
        except:
            print('Klucz nie jest liczbą z zakresu: 1..25')
            sys.exit(1)

def decrypt(method):
    with open(File['crypto']) as msg, open(File['key']) as key:
        try:
            key = int(next(key))
            if key not in range(1, 26):
                raise Exception()
            output = open(File['decrypt'], 'w')
            result = ''.join([ method.decrypt(letter, key) for letter in msg.read() ])
            output.write(result)
            output.close()
            print('Poprawnie odszyfrowano')
        except FileNotFoundError as err:
            print('Nie znaleziono pliku ' + err.filename)
        except:
            print('Klucz nie jest liczbą z zakresu: 1..25')
            sys.exit(1)

try:
    opts, args = getopt.getopt(sys.argv[1:], 'caedjk')
except getopt.GetoptError as err:
    print(err)
    sys.exit(1)

operation = None
method    = None

for o, a in opts:
    if   o == '-c':
        method = Caesar
    elif o == '-a':
        method = afinic
    elif o == '-e':
        operation = encrypt
    elif o == '-d':
        operation = decrypt
    elif o == '-j':
        pass
    elif o == '-k':
        pass

if operation is None or method is None:
    print('usage: ' + sys.argv[0] +  ' -[ac] -[edjk]')
    sys.exit(2)

operation(method)
