#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import getopt
import sys
import random as r


def write_key_tuple(filename, key_tuple):
    p, g, key = key_tuple
    with open(filename, 'w') as out:
        out.write(f'{p}\n')
        out.write(f'{g}\n')
        out.write(f'{key}\n')


def generate_keys():
    with open('elgamal.txt') as elgamal:
        p = int(elgamal.readline())
        g = int(elgamal.readline())
        private_key = r.randint(1, p - 1)
        public_key = pow(g, private_key, p)
        write_key_tuple('public.txt', (p, g, public_key))
        write_key_tuple('private.txt', (p, g, private_key))


def encrypt():
    with open('public.txt') as public, open('plain.txt') as plain:
        pass
    with open('crypto.txt', 'w') as crypto:
        pass


def decrypt():
    with open('private.txt') as private, open('crypto.txt') as crypto:
        pass
    with open('decrypt.txt', 'w') as decrypt:
        pass


def sign():
    with open('private.txt') as private, open('message.txt') as message:
        pass
    with open('signature.txt', 'w') as signature:
        pass


def verify():
    with open('public.txt') as public, open('message.txt') as message:
        pass
    with open('verify.txt', 'w') as verify:
        pass
    return True


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'deksv')
        if len(opts) != 1:
            raise getopt.GetoptError('')

        opt, _ = opts[0]
        if opt == '-k':
            generate_keys()
            print('Wygenerowano parę kluczy')
        elif opt == '-e':
            encrypt()
            print('Zaszyfrowano wiadomość')
        elif opt == '-d':
            decrypt()
            print('Odszyfrowano wiadomość')
        elif opt == '-s':
            sign()
            print('Wyprodukowano podpis')
        elif opt == '-v':
            v = verify()
            print('T' if v else 'N')
        else:
            raise getopt.GetoptError('')

    except getopt.GetoptError:
        print(f'użycie: {sys.argv[0]} -[deksv]')
        sys.exit(1)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(2)
    except ValueError as err:
        print(f'Niepoprawny format pliku elgamal.txt')
        sys.exit(3)


if __name__ == "__main__":
    main()
