#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

import sys
from string import ascii_letters, digits
from random import sample
from itertools import cycle
from hashlib import md5 as hash_fn
from PIL import Image, UnidentifiedImageError

BLOCK_WIDTH = 4
BLOCK_HEIGHT = 3


class WrongImageFormat(IOError):
    pass


def xor(pixel, key):
    (r, g, b) = pixel
    return (r ^ key, g ^ key, b ^ key)


def ecb(blocks, key):
    m = hash_fn(key.encode('utf-8'))
    it = cycle(m.digest())
    for block in blocks:
        yield (xor(pixel, next(it)) for pixel in block)


def cbc(blocks, key):
    m = hash_fn(key.encode('utf-8'))
    for block in blocks:
        m.update(str(block).encode('utf-8'))
        it = cycle(m.digest())
        yield (xor(pixel, next(it)) for pixel in block)


File = {
    'key':   'key.txt',
    'plain': 'plain.bmp',
    ecb:     'ecb_crypto.bmp',
    cbc:     'cbc_crypto.bmp'
}


def main():
    try:
        image = load_image(sys.argv[1] if len(sys.argv) > 1 else File['plain'])
        key = get_key()
        encrypt_image(image, ecb, key)
        print('Zakończono szyfrowanie w trybie EBC')
        encrypt_image(image, cbc, key)
        print('Zakończono szyfrowanie w trybie CBC')
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(1)
    except WrongImageFormat:
        print(f'Wystąpił błąd poczas wczytywania pliku {File["plain"]}')
        print(f'Czy plik na pewno został zapisany w formacie .bmp?')
        sys.exit(2)


def get_key():
    try:
        with open(File['key']) as key:
            return key.readline().strip()
    except FileNotFoundError:
        print(f'Nie znaleziono pliku: "{File["key"]}", wybrano losowy klucz')
        return ''.join(sample(ascii_letters + digits, 32))


def load_image(file_path):
    try:
        with Image.open(file_path, formats=['BMP']) as image:
            image = image.crop(adjusted_size(image))
            image = image.convert('RGB')
            return image
    except (UnidentifiedImageError, TypeError):
        raise WrongImageFormat


# (0, 0, width + (-width % BLOCK_WIDTH), height + (-height % BLOCK_HEIGHT))
def adjusted_size(image):
    (width, height) = image.size
    if (width % BLOCK_WIDTH) != 0 or (height % BLOCK_HEIGHT) != 0:
        width -= width % BLOCK_WIDTH
        height -= height % BLOCK_HEIGHT
        print(f'Wielkość obrazu nie dzieli się równo na bloki '
              f'{BLOCK_WIDTH}x{BLOCK_HEIGHT}')
        print(f'Zaokrąglono wymary do {width}x{height}')
    return (0, 0, width, height)


def encrypt_image(image, algorithm, key):
    blocks = blockify(image)
    save_image_blocks(algorithm(blocks, key), image.size, File[algorithm])


def blockify(image):
    return ((image.getpixel(pixel) for pixel in block)
            for block in block_iterator(image.size))


def block_iterator(size):
    (width, height) = size
    return (block_at(x, y)
            for x in range(0, width, BLOCK_WIDTH)
            for y in range(0, height, BLOCK_HEIGHT))


def block_at(x0, y0):
    return ((x0 + dx, y0 + dy)
            for dx in range(BLOCK_WIDTH)
            for dy in range(BLOCK_HEIGHT))


def save_image_blocks(blocks, size, file_path):
    with open(file_path, 'wb') as output:
        image = Image.new('RGB', size)

        for block, coords in zip(blocks, block_iterator(size)):
            for pixel, coord in zip(block, coords):
                image.putpixel(coord, pixel)
        image.save(output)


if __name__ == "__main__":
    main()
