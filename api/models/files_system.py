import datetime
from typing import List

from fastapi_camelcase import CamelModel

from files_system.constants import ItemType


class Item(CamelModel):
    name: str
    modified_at: datetime.datetime
    created_at: datetime.datetime
    absolute_path: str
    type: ItemType
    byte_size: int


class File(Item):
    content: str


class DirectoryNoItems(Item):
    pass


class Directory(Item):
    items_list: List[File | DirectoryNoItems]


class UpdateFileContentRequestBody(CamelModel):
    content: str


class RenameItemRequestBody(CamelModel):
    name: str
