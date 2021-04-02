#!/usr/bin/env python3
#
# Autorem skryptu jest Grzegorz Chojnacki
# Skrypt został sprawdzony na wersji pythona 3.9.2
#

from PIL import Image
import sys

BLOCK_WIDTH = 4
BLOCK_HEIGHT = 3

IMAGE_SIZE = None

File = {
    'key':   'key.txt',
    'plain': 'plain.bmp',
    'ecb':   'ecb_crypto.bmp',
    'cbc':   'cbc_crypto.bmp',
}


def adjust_size(size):
    (width, height) = size
    return (0, 0, width - (width % BLOCK_WIDTH), height - (height % BLOCK_HEIGHT))


def load_image_blocks():
    global IMAGE_SIZE
    with Image.open(File['plain']) as image:
        image = image.crop(adjust_size(image.size))
        IMAGE_SIZE = image.size
        return [[image.getpixel(pixel) for pixel in block]
                for block in block_iterator(image.size)]


def block_iterator(size):
    (width, height) = size
    return (make_block(x, y) for x in range(0, width, BLOCK_WIDTH) for y in range(0, height, BLOCK_HEIGHT))


def make_block(x0, y0):
    return [(x0 + dx, y0 + dy) for dx in range(BLOCK_WIDTH) for dy in range(BLOCK_HEIGHT)]


# ToDo: load key from file
def get_key():
    return 0


def ecb(blocks, key):
    return blocks


def cbc(blocks, key):
    return blocks


def save_image_blocks(blocks, file_path):
    with open(file_path, 'wb') as output:
        image = Image.new('RGB', IMAGE_SIZE)

        for block, coords in zip(blocks, block_iterator(IMAGE_SIZE)):
            for pixel, coord in zip(block, coords):
                image.putpixel(coord, pixel)
        image.save(output)


def main():
    try:
        blocks = load_image_blocks()
        key = get_key()
        save_image_blocks(ecb(blocks, key), File['ecb'])
        save_image_blocks(cbc(blocks, key), File['ecb'])
    except FileNotFoundError as err:
        print(f'Nie znaleziono pliku: "{err.filename}"')
        sys.exit(1)


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
