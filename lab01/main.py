#!/usr/bin/env python3
import getopt
import sys
import math
import caesar
import affine

File = {
    'plain':     'plain.txt',
    'crypto':    'crypto.txt',
    'decrypt':   'decrypt.txt',
    'key':       'key.txt',
    'extra':     'extra.txt',
    'key_found': 'key-found.txt',
}


def write_algorithm_output(algorithm, key, output, text):
    result = [algorithm(letter, key) for letter in text]
    output.write(''.join(result))


def transform(method, algorithm, input_file, output_file):
    with (open(input_file) as text,
          open(File['key']) as key,
          open(output_file, 'w') as output):
        key = method.parse_key(key.read().strip())
        write_algorithm_output(algorithm, key, output, text.read())


def encrypt(method):
    transform(method, method.encrypt, File['plain'], File['crypto'])
    print('Poprawnie zaszyfrowano')


def decrypt(method):
    transform(method, method.decrypt, File['crypto'], File['decrypt'])
    print('Poprawnie odszyfrowano')


def brute_force(method):
    with (open(File['crypto']) as crypto,
          open(File['decrypt'], 'w') as output):
        crypto = crypto.read().strip()
        for key in method.key_range():
            output.write(f'### Key: {key}\n')
            write_algorithm_output(method.decrypt, key, output, crypto)
            output.write('\n\n')
        print('Zakończono odszyfrowywanie')


def find_key(method):
    with (open(File['crypto']) as crypto,
          open(File['extra']) as extra,
          open(File['decrypt'], 'w') as output,
          open(File['key_found'], 'w') as key_found):
        crypto = crypto.read().strip()
        extra = extra.read().strip()
        keys = set.intersection(*[method.find_key(pair)
                                  for pair in zip(extra, crypto)])
        assert len(keys) == 1
        key = keys.pop()
        key_found.write(method.key_str(key))
        write_algorithm_output(method.decrypt, key, output, crypto)
        print('Znaleziono pasujący klucz')


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'caedjk')
        operation = method = None
        for o, _ in opts:
            if o == '-c':
                method = caesar
            elif o == '-a':
                method = affine
            elif o == '-e':
                operation = encrypt
            elif o == '-d':
                operation = decrypt
            elif o == '-j':
                operation = find_key
            elif o == '-k':
                operation = brute_force

        if operation is None or method is None:
            print(f'użycie: {sys.argv[0]} -[ac] -[edjk]')
            sys.exit(1)
        else:
            operation(method)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: \"{err.filename}\"')
        sys.exit(3)
    except ValueError as err:
        print(f'Zły format klucza: \"{err}\"')
        sys.exit(4)
    except AssertionError:
        print('Nie udało się jednoznacznie rozszyfrować')
        sys.exit(5)


if __name__ == "__main__":
    main()
