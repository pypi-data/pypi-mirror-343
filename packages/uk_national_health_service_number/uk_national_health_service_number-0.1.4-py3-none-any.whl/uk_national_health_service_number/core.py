from ._internal import _generate_nhs_number
import itertools

class NHSNumberGenerator:
    def __init__(self, num_records: int = 1):
        self.num_records = num_records

    def generate_uk_national_health_service_number(self):
        return list(itertools.starmap(lambda *_: _generate_nhs_number(), zip(range(self.num_records))))