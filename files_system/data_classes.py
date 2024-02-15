import datetime
from typing import Optional

from files_system.constants import ItemType


class BaseItem:
    def __init__(self, name: str, parent_directory: Optional['Directory'] = None) -> None:
        self.name = name
        self.parent_directory = parent_directory
        self.modified_at = datetime.datetime.now(tz=datetime.UTC)
        self.created_at = datetime.datetime.now(tz=datetime.UTC)
        self.absolute_path = self.get_absolute_path()

    def get_absolute_path(self):
        absolute_path = self.name if self.name else '/'
        current_item = self.parent_directory
        while current_item is not None:
            absolute_path = current_item.name + '/' + absolute_path
            current_item = current_item.parent_directory
        return absolute_path


class Directory(BaseItem):
    def __init__(self, name: str, parent_directory: Optional['Directory'] = None) -> None:
        self.items = dict()
        super().__init__(name, parent_directory)

    @property
    def byte_size(self):
        return sum(item.byte_size for item in self.items.values())

    @property
    def type(self):
        return ItemType.DIRECTORY

    @property
    def items_list(self):
        return self.items.values()


class File(BaseItem):
    def __init__(self, name: str, content: str, byte_size: int, parent_directory:  Optional[Directory] = None) -> None:
        self.content = content
        self.byte_size = byte_size
        super().__init__(name, parent_directory)

    @property
    def type(self):
        return ItemType.FILE
