import random

from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic.alias_generators import to_camel

from files_system.data_classes import File, Directory
from api.models.files_system import File as PydanticFile, Directory as PydanticDirectory, DirectoryNoItems
from files_system.utils import is_file, is_directory


def file_to_pydantic_file(item: File) -> PydanticFile:
    return PydanticFile(
        name=item.name,
        created_at=item.created_at,
        modified_at=item.modified_at,
        absolute_path=item.absolute_path,
        type=item.type,
        byte_size=item.byte_size,
        content=item.content,
    )


def directory_to_pydantic_directory_no_items(item: Directory, calculate_directories_size: bool) -> DirectoryNoItems:
    return DirectoryNoItems(
        name=item.name,
        created_at=item.created_at,
        modified_at=item.modified_at,
        absolute_path=item.absolute_path,
        type=item.type,
        byte_size=item.byte_size if calculate_directories_size else 0,
    )


def item_to_pydantic_item_in_list(
        item: File | Directory,
        calculate_directories_size: bool = False
) -> PydanticFile | DirectoryNoItems:
    if is_file(item):
        return file_to_pydantic_file(item)

    if is_directory(item):
        return directory_to_pydantic_directory_no_items(item, calculate_directories_size)


def directory_to_pydantic_directory(item: Directory, calculate_directories_size: bool) -> PydanticDirectory:
    return PydanticDirectory(
        name=item.name,
        created_at=item.created_at,
        modified_at=item.modified_at,
        absolute_path=item.absolute_path,
        type=item.type,
        byte_size=item.byte_size if calculate_directories_size else 0,
        items_list=[
            item_to_pydantic_item_in_list(item_in_list) for item_in_list in item.items_list
        ]
    )


def item_to_pydantic_model(
    item: File | Directory,
    calculate_directories_size: bool = False
) -> PydanticFile | PydanticDirectory:
    if is_file(item):
        return file_to_pydantic_file(item)

    if is_directory(item):
        return directory_to_pydantic_directory(item, calculate_directories_size)


def camelize_query_parameters_with_no_custom_alias(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            for param in route.dependant.query_params:
                if param.alias == param.name:
                    param.field_info.alias = to_camel(param.name)


def generate_default_file_size() -> int:
    return random.randint(1, 10000)


def generate_default_file_name(parent_directory: Directory) -> str:
    name = "New File"
    count = 1
    while parent_directory.items.get(name) is not None:
        name = f"New File ({count})"
        count += 1
    return name


def generate_default_directory_name(parent_directory: Directory) -> str:
    name = "New Folder"
    count = 1
    while parent_directory.items.get(name) is not None:
        name = f"New Folder ({count})"
        count += 1
    return name
