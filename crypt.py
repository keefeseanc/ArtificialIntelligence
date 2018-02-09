#solves upper case puzzles
#example solve("SEND + MORE == MONEY")

import itertools
import re
import string

def solve(puzzle):
    copy, letters = numbers(puzzle)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        if copy(*digits) is True:
            table = string.maketrans(letters, ''.join(map(str, digits)))
            return puzzle.translate(table)

def numbers(puzzle):
    letters = ''.join(set(re.findall('[A-Z]', puzzle)))
    string = ', '.join(letters)
    token = map(word, re.split('([A-Z]+)', puzzle))
    body = ''.join(token)
    copy = 'lambda %s: %s' % (string, body)
    return eval(copy), letters

def word(word):
    if word.isupper():
        terms = [('%s*%s' % (10**i, d))
                for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word
