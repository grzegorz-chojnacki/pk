#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import getopt
import sys
from math import gcd
from random import randint


def read_lines(filename, n=1):
    with open(filename) as src:
        if n == 1:
            return int(next(src))
        else:
            return tuple(int(next(src)) for i in range(0, n))


def write_lines(filename, values):
    with open(filename, 'w') as out:
        for value in values:
            out.write(f'{value}\n')


def generate_keys(p, g):
    private_key = randint(1, p - 1)
    public_key = pow(g, private_key, p)
    return (private_key, public_key)


def encrypt(msg, p, g, key):
    assert msg < p
    encryption_key = randint(1, p - 1)

    shadow = pow(g, encryption_key, p)
    cryptogram = msg * pow(key, encryption_key, p) % p
    return [shadow, cryptogram]


def decrypt(crypto_msg, crypto_key, p, key):
    shadow = pow(crypto_key, key, p)
    e = pow(shadow, -1, p)
    return crypto_msg * e % p


def random_coprime(p):
    while True:
        sign_key = randint(2, p - 1)
        if gcd(sign_key, p) == 1:
            yield sign_key


def sign(msg, p, g, key):
    assert msg < p

    sign_key = next(random_coprime(p - 1))
    sign_key_e = pow(sign_key, -1, p - 1)
    r = pow(g, sign_key, p)
    x = (msg - key * r) * sign_key_e % (p - 1)
    return [r, x]


def verify(msg, r, x, p, g, key):
    exp1 = pow(g, msg, p)
    exp2 = pow(r, x, p) * pow(key, r, p) % p
    return exp1 == exp2


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'deksv')
        if len(opts) != 1:
            raise getopt.GetoptError('')

        opt, _ = opts[0]
        if opt == '-k':
            (p, g) = read_lines('elgamal.txt', 2)
            (private, public) = generate_keys(p, g)

            write_lines('public.txt', [p, g, public])
            write_lines('private.txt', [p, g, private])
            print('Wygenerowano parę kluczy')

        elif opt == '-e':
            msg = read_lines('plain.txt')
            (p, g, key) = read_lines('public.txt', 3)

            write_lines('crypto.txt', encrypt(msg, p, g, key))
            print('Zaszyfrowano wiadomość')

        elif opt == '-d':
            (crypto_key, crypto_msg) = read_lines('crypto.txt', 2)
            (p, _, key) = read_lines('private.txt', 3)

            msg = decrypt(crypto_msg, crypto_key, p, key)
            write_lines('decrypt.txt', [msg])
            print('Odszyfrowano wiadomość')

        elif opt == '-s':
            msg = read_lines('message.txt')
            (p, g, key) = read_lines('private.txt', 3)

            write_lines('signature.txt', sign(msg, p, g, key))
            print('Wyprodukowano podpis')

        elif opt == '-v':
            msg = read_lines('message.txt')
            (r, x) = read_lines('signature.txt', 2)
            (p, g, key) = read_lines('public.txt', 3)

            result = 'T' if verify(msg, r, x, p, g, key) else 'N'
            write_lines('verify.txt', [result])
            print(result)
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
        sys.exit(4)


if __name__ == "__main__":
    main()
