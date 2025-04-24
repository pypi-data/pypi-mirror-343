# Thai Identity Number Generator

This package generates random valid Thai National Identity Numbers (13-digit) for testing

## Installation

You can install the package via Poetry:

```bash
poetry add thai-identity-generator
```

## Usage
```
from thai_identity_generator import generate_thailand_identity_number

# Generate a list of Thai ID numbers
nric_numbers = generate_thailand_identity_number(num_records=5)

for nric in nric_numbers:
    print(nric)```