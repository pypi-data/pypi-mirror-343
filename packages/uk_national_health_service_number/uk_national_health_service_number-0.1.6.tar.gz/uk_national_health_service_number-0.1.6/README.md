# uk_national_health_service_number

![PyPI](https://img.shields.io/pypi/v/uk_national_health_service_number)
![Python](https://img.shields.io/pypi/pyversions/uk_national_health_service_number)

A Python package to **generate valid UK NHS numbers** using the official modulus-11 checksum algorithm for testing 

---

## ✨ Features

- ✅ Generate one or more valid NHS numbers
- 📦 Easy-to-use Python API
- 🧪 Includes unit tests

---

## 🚀 Installation

Install from [PyPI](https://pypi.org/project/uk-national-health-service-number/):

```bash
pip install uk_national_health_service_number

---
## 🧪 Usage

### ▶️ In Python

Generate NHS numbers programmatically:

```python
from uk_national_health_service_number import NHSNumberGenerator

# Generate 3 NHS numbers
gen = NHSNumberGenerator(num_records=3)
numbers = gen.generate_uk_national_health_service_number()

for number in numbers:
    print(number)