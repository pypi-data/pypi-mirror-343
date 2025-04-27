# GSTIN Validator

A Python package for validating Indian GSTIN numbers

## Installation

```bash

pip install gstin-validator

```

## usage

```bash
from gstin_validator.core import validate_gstin

is_valid=validate_gstin("GSTI_NUMER")
print(is_valid) #prints True if valid else false 

```