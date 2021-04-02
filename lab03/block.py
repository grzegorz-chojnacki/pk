#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import sys
import itertools as it
from itertools import cycle
from hashlib import md5
from PIL import Image

BLOCK_WIDTH = 4
BLOCK_HEIGHT = 4


def encrypt(pixel, key):
    (r, g, b) = pixel
    return (r ^ key, g ^ key, b ^ key)

def ecb(blocks, key):
    it = cycle(md5(key.encode('utf-8')).digest())
    for block in blocks:
        yield [encrypt(pixel, next(it)) for pixel in block]

def cbc(blocks, key):
    return blocks


def rgb_to_bw(pixel):
    return chr(sum(pixel) // 3).encode('utf-8')


File = {
    'key':   'key.txt',
    'plain': 'plain.bmp',
    ecb:     'ecb_crypto.bmp',
    cbc:     'cbc_crypto.bmp'
}


def main():
    try:
        key = get_key()
        encrypt_image(ecb, key)
        # encrypt_image(cbc, key)
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(1)


def get_key():
    return 'bgfi8nm4DCZ3wOxW4UfYDvFJsnHd4PJ7'


def encrypt_image(algorithm, key):
    with Image.open(File['plain']) as image:
        image = image.crop(adjusted_size(image))
        blocks = blockify(image)
        save_image_blocks(algorithm(blocks, key), image.size, File[algorithm])


# (0, 0, width + (-width % BLOCK_WIDTH), height + (-height % BLOCK_HEIGHT))
def adjusted_size(image):
    (width, height) = image.size
    return (0, 0, width - (width % BLOCK_WIDTH), height - (height % BLOCK_HEIGHT))


def blockify(image):
    return [[image.getpixel(pixel) for pixel in block]
            for block in block_iterator(image.size)]


def block_iterator(size):
    (width, height) = size
    return (make_block(x, y)
            for x in range(0, width, BLOCK_WIDTH)
            for y in range(0, height, BLOCK_HEIGHT))


def make_block(x0, y0):
    return [(x0 + dx, y0 + dy) for dx in range(BLOCK_WIDTH) for dy in range(BLOCK_HEIGHT)]


def save_image_blocks(blocks, size, file_path):
    with open(file_path, 'wb') as output:
        image = Image.new('RGB', size)

        for block, coords in zip(blocks, block_iterator(size)):
            for pixel, coord in zip(block, coords):
                image.putpixel(coord, pixel)
        image.save(output)


if __name__ == "__main__":
    main()

'''
- Wczytać obrazek
    - Sprawdzić wymiary i wykadrować w razie co
    - podzielić obrazek na bloki
    - Zwrócić liste bloków
- Wczytać opcjonalny klucz
- Zakodować bloki za pomocą ecb i cbc
- Spłaszczyć bloki do dobrego formatu
- Zapisać obrazki
'''
