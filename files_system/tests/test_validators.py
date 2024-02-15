import pytest
from files_system.validators import validate_item_name, validate_file_size
from files_system.constants import PROHIBITED_NAME_SYMBOLS
from files_system.exceptions import EmptyItemNameException, ProhibitedSymbolInItemNameException, \
    NotPositiveFileSizeException


def test_validate_item_name_correct_name():
    assert validate_item_name('test.txt') is None


def test_validate_item_name_empty_name():
    with pytest.raises(EmptyItemNameException):
        validate_item_name('')


def test_validate_item_name_prohibited_symbols():
    for prohibited_symbol in PROHIBITED_NAME_SYMBOLS:
        with pytest.raises(ProhibitedSymbolInItemNameException):
            validate_item_name(f'test{prohibited_symbol}')


def test_validate_file_size_positive():
    assert validate_file_size(123) is None


def test_validate_file_size_zero():
    with pytest.raises(NotPositiveFileSizeException):
        validate_file_size(0)


def test_validate_file_size_negative():
    with pytest.raises(NotPositiveFileSizeException):
        validate_file_size(-123)
