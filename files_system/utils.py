from typing import List, Tuple

from files_system.constants import ItemType, SortableItemFields
from files_system.data_classes import File, Directory
from files_system.exceptions import NotStartingWithSlashPathException, EmptyPathException, SortByThisFieldNotSupported
from files_system.validators import validate_sort_field


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


def get_item_field_from_sort_field(
    item: File | Directory,
    sort_field: str,
    calculate_directories_size: bool
):
    validate_sort_field(sort_field)
    if sort_field == 'byte_size':
        if is_directory(item) and not calculate_directories_size:
            return 0
        else:
            return item.byte_size

    if sort_field == 'name':
        return item.name

    if sort_field == 'created_at':
        return item.created_at

    if sort_field == 'modified_at':
        return item.modified_at

    return 0


def get_items_sort_function(sort_fields: List[str], calculate_directories_size: bool):
    def sort_function(item: File | Directory):
        return [
            get_item_field_from_sort_field(item, sorting_tuple, calculate_directories_size)
            for sorting_tuple in sort_fields
        ]
    return sort_function
