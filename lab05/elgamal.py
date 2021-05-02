#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import getopt
import sys
import math as m
import random as r


def read_lines(filename):
    with open(filename) as src:
        return tuple(int(n) for n in src.readlines())


def write_lines(filename, payload):
    with open(filename, 'w') as out:
        for value in payload:
            out.write(f'{value}\n')


def generate_keys():
    (p, g) = read_lines('elgamal.txt')

    private_key = r.randint(1, p - 1)
    public_key = pow(g, private_key, p)

    write_lines('public.txt', [p, g, public_key])
    write_lines('private.txt', [p, g, private_key])


def encrypt():
    (msg,) = read_lines('plain.txt')
    (p, g, public_key) = read_lines('public.txt')

    assert msg < p
    encryption_key = r.randint(1, p - 1)

    shadow = pow(g, encryption_key, p)
    cryptogram = msg * pow(public_key, encryption_key, p) % p
    write_lines('crypto.txt', [shadow, cryptogram])


def decrypt():
    (crp_key, crp_msg) = read_lines('crypto.txt')
    (p, _, private_key) = read_lines('private.txt')

    shadow = pow(crp_key, private_key, p)
    e = pow(shadow, -1, p)
    msg = crp_msg * e % p

    write_lines('decrypt.txt', [msg])


def random_coprime(p):
    while True:
        sign_key = r.randint(2, p - 1)
        if m.gcd(sign_key, p) == 1:
            yield sign_key


def sign():
    (msg,) = read_lines('message.txt')
    (p, g, private_key) = read_lines('private.txt')

    assert msg < p

    sign_key = next(random_coprime(p - 1))
    sign_key_e = pow(sign_key, -1, p - 1)
    r = pow(g, sign_key, p)
    x = (msg - private_key * r) * sign_key_e % (p - 1)

    write_lines('signature.txt', [r, x])


def verify():
    (msg,) = read_lines('message.txt')
    (r, x) = read_lines('signature.txt')
    (p, g, public_key) = read_lines('public.txt')

    left = pow(g, msg, p)
    right = pow(r, x, p) * pow(public_key, r, p) % p

    result = 'T' if left == right else 'N'
    write_lines('verify.txt', [result])

    return result


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
            print(verify())
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
