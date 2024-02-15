from enum import Enum

PROHIBITED_NAME_SYMBOLS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']


class ItemType(Enum):
    FILE = "FILE"
    DIRECTORY = "DIRECTORY"


SortableItemFields = ['name', 'byte_size', 'created_at', 'modified_at']
