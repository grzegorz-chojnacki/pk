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
        p = int(public.readline())
        g = int(public.readline())
        public_key = int(public.readline())
        msg = int(plain.readline())

        assert msg < p
        encryption_key = r.randint(1, p - 1)

    with open('crypto.txt', 'w') as crypto:
        crypto.write(f'{pow(g, encryption_key, p)}\n')
        crypto.write(f'{msg * pow(public_key, encryption_key, p) % p}\n')


def decrypt():
    with open('private.txt') as private, open('crypto.txt') as crypto:
        p = int(private.readline())
        g = int(private.readline())
        private_key = int(private.readline())
        crp_key = int(crypto.readline())
        crp_msg = int(crypto.readline())

        shadow = pow(crp_key, private_key, p)
        e = pow(shadow, -1, p)
        msg = crp_msg * e % p

    with open('decrypt.txt', 'w') as decrypt:
        decrypt.write(f'{msg}\n')


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
    except ValueError:
        print(f'Niepoprawny format pliku')
        sys.exit(3)
    except AssertionError:
        print(f'Szyfrowana wiadomość nie spełnia warunku: m < p')
        sys.exit(3)


if __name__ == "__main__":
    main()
