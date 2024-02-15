from typing import List, Tuple

from files_system.constants import ItemType, SortableItemFields
from files_system.data_classes import File, Directory
from files_system.exceptions import NotStartingWithSlashPathException, EmptyPathException, SortByThisFieldNotSupported


def get_items_names_from_path(path) -> List[str]:
    if len(path) == 0:
        raise EmptyPathException
    if path[0] != '/':
        raise NotStartingWithSlashPathException
    if path[-1] == '/':
        path = path[:-1]
    items_names = path.split('/')[1:]
    return items_names


def is_directory(item: File | Directory) -> bool:
    return item.type == ItemType.DIRECTORY


def is_file(item: File | Directory) -> bool:
    return item.type == ItemType.FILE


def get_sorting_tuple_from_sort_field(sort_field: str) -> Tuple[str, bool]:
    sorting_tuple = (sort_field[1:], True) if sort_field.startswith('-') else (sort_field, False)
    if sorting_tuple[0] not in SortableItemFields:
        raise SortByThisFieldNotSupported(sort_field)
    return sorting_tuple


def get_item_field_from_sorting_tuple(
    item: File | Directory,
    sorting_tuple: Tuple[str, bool],
    calculate_directories_size: bool
):
    value = 0
    if sorting_tuple[0] == 'byte_size':
        if is_directory(item) and not calculate_directories_size:
            value = 0
        else:
            value = item.byte_size

    if sorting_tuple[0] == 'name':
        value = item.name

    if sorting_tuple[0] == 'created_at':
        value = item.created_at

    if sorting_tuple[0] == 'modified_at':
        value = item.modified_at

    if sorting_tuple[1]:
        return -value
    return value


def get_items_sort_function(sort_fields: Tuple[str], calculate_directories_size: bool):
    sorting_tuples = [get_sorting_tuple_from_sort_field(sort_field) for sort_field in sort_fields]

    def sort_function(item: File | Directory):
        return [
            get_item_field_from_sorting_tuple(item, sorting_tuple, calculate_directories_size)
            for sorting_tuple in sorting_tuples
        ]
    return sort_function
