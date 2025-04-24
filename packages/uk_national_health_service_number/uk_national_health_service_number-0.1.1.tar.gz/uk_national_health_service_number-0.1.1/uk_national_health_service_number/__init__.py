import functools
import itertools
import random


class NHSNumberGenerator:
    def __init__(self, num_records=1):
        self.num_records = num_records

    def generate_uk_national_health_service_number(self):
        def _ɢ(x):
            return functools.reduce(lambda a, b: a + b, map(lambda i: i[0] * i[1], zip(x, range(10, 1, -1))))

        def _χ(x):
            r = 11 - (_ɢ(x) % 11)
            return {10: None, 11: 0}.get(r, r)

        def _η():
            while True:
                α = list(itertools.starmap(lambda *_: random.randint(0, 9), zip(range(9), range(9))))
                β = _χ(α)
                if β is not None:
                    return ''.join(map(str, α + [β]))

        return list(itertools.starmap(lambda *_: _η(), zip(range(self.num_records))))