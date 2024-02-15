from files_system.exceptions import EmptyItemNameException, ProhibitedSymbolInItemNameException, \
    NotPositiveFileSizeException, EmptySearchKeywordException
from files_system.constants import PROHIBITED_NAME_SYMBOLS


def validate_item_name(name):
    if len(name) == 0:
        raise EmptyItemNameException

    if any(prohibited_symbol in name for prohibited_symbol in PROHIBITED_NAME_SYMBOLS):
        raise ProhibitedSymbolInItemNameException


def validate_file_size(size):
    if size <= 0:
        raise NotPositiveFileSizeException


def validate_search_keyword(keyword):
    if len(keyword) == 0:
        raise EmptySearchKeywordException
