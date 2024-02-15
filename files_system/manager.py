import datetime
from typing import List, Tuple
from collections import deque

from files_system.data_classes import Directory, File
from files_system.exceptions import ItemAlreadyExistsOnCreateException, ItemNotFoundException, \
    DeleteRootDirectoryException, \
    FileNotFoundException, DirectoryNotFoundException, ItemAlreadyExistsOnRenameException
from files_system.utils import get_items_names_from_path, is_directory, is_file, get_items_sort_function
from files_system.validators import validate_item_name, validate_file_size, validate_search_keyword


class FilesSystemManager:
    def __init__(self):
        self.root = Directory(name="")

    @staticmethod
    def __update_parents_modified_at(item: File | Directory, modification_time: datetime.datetime) -> None:
        current_parent = item.parent_directory
        while current_parent:
            current_parent.modified_at = modification_time
            current_parent = current_parent.parent_directory

    def __handle_item_modification(self, item: File | Directory):
        modification_time = datetime.datetime.now(tz=datetime.UTC)
        item.modified_at = modification_time
        self.__update_parents_modified_at(item, modification_time)

    def __create_item(
        self,
        parent_path: str,
        name: str,
        item_type: type[File] | type[Directory],
        *args,
        **kwargs
    ) -> File | Directory:
        validate_item_name(name)
        parent_directory = self.get_directory_from_path(parent_path)
        if parent_directory.items.get(name):
            raise ItemAlreadyExistsOnCreateException(parent_path, name)
        item = item_type(name=name, parent_directory=parent_directory, *args, **kwargs)
        parent_directory.items[name] = item
        self.__update_parents_modified_at(item, item.created_at)
        return item

    def create_file(self, parent_path: str, name: str, content: str, byte_size) -> File:
        validate_file_size(byte_size)
        return self.__create_item(
            parent_path=parent_path, name=name, item_type=File, content=content, byte_size=byte_size
        )

    def create_directory(self, parent_path: str, name: str) -> Directory:
        return self.__create_item(parent_path=parent_path, name=name, item_type=Directory)

    def get_item_from_path(self, path: str) -> File | Directory:
        items_names = get_items_names_from_path(path)
        item = self.root
        for item_name in items_names:
            if not is_directory(item) or not item.items.get(item_name):
                raise ItemNotFoundException(path)
            item = item.items[item_name]
        return item

    def get_directory_from_path(self, path: str) -> Directory:
        item = self.get_item_from_path(path)
        if not is_directory(item):
            raise DirectoryNotFoundException(path)
        return item

    def get_file_from_path(self, path: str) -> File:
        item = self.get_item_from_path(path)
        if not is_file(item):
            raise FileNotFoundException(path)
        return item

    def rename_item(self, path: str, new_name: str) -> File:
        validate_item_name(new_name)
        item = self.get_item_from_path(path)
        if item.parent_directory.items.get(new_name):
            raise ItemAlreadyExistsOnRenameException(path, new_name)
        item.parent_directory.items[new_name] = item
        del item.parent_directory.items[item.name]
        item.name = new_name
        item.absolute_path = item.get_absolute_path()

        self.__handle_item_modification(item)
        return item

    def update_file_content(self, path: str, new_content: str) -> File:
        file = self.get_file_from_path(path)
        file.content = new_content
        self.__handle_item_modification(file)
        return file

    def delete_item(self, path: str) -> None:
        item = self.get_item_from_path(path)
        if not item.parent_directory:
            raise DeleteRootDirectoryException()
        del item.parent_directory.items[item.name]
        self.__update_parents_modified_at(item, datetime.datetime.now(tz=datetime.UTC))

    def search_items_by_keyword(
        self,
        keyword: str,
        search_directory_path='/'
    ) -> List[File | Directory]:
        validate_search_keyword(keyword)
        found_items = []
        start_point = self.get_directory_from_path(search_directory_path)
        items_queue = deque(start_point.items.values())
        while len(items_queue) != 0:
            item = items_queue.popleft()
            if is_directory(item):
                items_queue.extend(item.items.values())
                if keyword in item.name:
                    found_items.append(item)
                continue

            if is_file(item):
                if keyword in item.name or keyword in item.content:
                    found_items.append(item)
                continue

        return found_items

    def list_items_with_sorting(
        self,
        directory_path: str = '/',
        include_inner: bool = False,
        sort_fields: List[str] = (),
        descending: bool = False,
        calculate_directories_size: bool = False
    ):
        directory = self.get_directory_from_path(directory_path)
        if include_inner:
            items = []
            start_point = directory
            items_queue = deque(start_point.items.values())
            while len(items_queue) != 0:
                item = items_queue.popleft()
                if is_directory(item):
                    items_queue.extend(item.items.values())

                items.append(item)

        else:
            items = directory.items

        return sorted(items, key=get_items_sort_function(sort_fields, calculate_directories_size), reverse=descending)

