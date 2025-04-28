import pytest
from il_bank_validator import validate_israeli_bank_account

def test_valid_leumi():
    assert validate_israeli_bank_account(10, 936, "07869660") == True

def test_invalid_account():
    assert validate_israeli_bank_account(10, 936, "00000000") == False
