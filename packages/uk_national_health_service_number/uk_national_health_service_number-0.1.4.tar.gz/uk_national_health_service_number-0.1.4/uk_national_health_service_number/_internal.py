import random
import functools
import itertools

def _modulus_11_check(x):
    return functools.reduce(lambda a, b: a + b, map(lambda i: i[0] * i[1], zip(x, range(10, 1, -1))))

def _checksum(x):
    r = 11 - (_modulus_11_check(x) % 11)
    return {10: None, 11: 0}.get(r, r)

def _generate_nhs_number():
    while True:
        base = [random.randint(0, 9) for _ in range(9)]
        check = _checksum(base)
        if check is not None:
            return ''.join(map(str, base + [check]))