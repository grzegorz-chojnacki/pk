ALPHABET_SIZE = 26


def case_offset(letter):
    if letter.isupper():
        return ord('A')
    else:
        return ord('a')
