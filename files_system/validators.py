from files_system.exceptions import EmptyItemNameException, ProhibitedSymbolInItemNameException, \
    NotPositiveFileSizeException, EmptySearchKeywordException, SortByThisFieldNotSupported
from files_system.constants import PROHIBITED_NAME_SYMBOLS, SortableItemFields


def validate_item_name(name) -> None:
    if len(name) == 0:
        raise EmptyItemNameException

    if any(prohibited_symbol in name for prohibited_symbol in PROHIBITED_NAME_SYMBOLS):
        raise ProhibitedSymbolInItemNameException


def validate_file_size(size) -> None:
    if size <= 0:
        raise NotPositiveFileSizeException


def validate_search_keyword(keyword) -> None:
    if len(keyword) == 0:
        raise EmptySearchKeywordException


def validate_sort_field(sort_field: str) -> None:
    if sort_field not in SortableItemFields:
        raise SortByThisFieldNotSupported(sort_field)
