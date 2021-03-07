File = {
    'plain':     'plain.txt',
    'crypto':    'crypto.txt',
    'decrypt':   'decrypt.txt',
    'key':       'key.txt',
    'extra':     'extra.txt',
    'key_found': 'key-found.txt',
}

ALPHABET_SIZE = 26


def case_offset(letter):
    if letter.isupper():
        return ord('A')
    else:
        return ord('a')
