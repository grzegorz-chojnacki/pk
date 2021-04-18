#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

from os.path import isfile
import subprocess as sp

File = {
    'A': 'personal.txt',
    'B': 'personal_.txt',
    'pdf': 'hash.pdf',
}

fns = [
    'md5sum',
    'sha1sum',
    'sha224sum',
    'sha256sum',
    'sha384sum',
    'sha512sum',
    'b2sum',
]


def checksum_pdf(file, fn, out):
    cat = sp.Popen(['cat', file, File['pdf']], stdout=sp.PIPE)
    output = sp.check_output(fn, stdin=cat.stdout, text=True)
    out.write(f"cat {file.ljust(13)} {File['pdf']} | {fn}\n")
    return output[:-4]


for file in File.values():
    if not isfile(file):
        print(f'Nie znaleziono pliku "{file}"')
        exit(1)

with open('diff.txt', 'w') as out:
    for fn in fns:
        sumA = checksum_pdf(File['A'], fn, out)
        sumB = checksum_pdf(File['B'], fn, out)
        out.write(sumA + '\n')
        out.write(sumB + '\n')

        diff = bin(int(sumA, 16) ^ int(sumB, 16))[2:]

        diff_bits = diff.count('1')
        diff_len = len(diff)
        diff_percent = round(diff_bits / diff_len * 100, 2)

        out.write('Liczba różniących się bitów: ')
        out.write(f"{diff_bits}/{diff_len}, {diff_percent}%\n\n")
