from typing import Annotated, List

from fastapi import APIRouter, Depends

from api.dependencies import get_files_system_manager
from api.models.files_system import File, DirectoryNoItems
from api.utils import item_to_pydantic_item_in_list, generate_default_directory_name
from files_system.manager import FilesSystemManager

router = APIRouter(prefix='/directory')


@router.get('/search', response_model=List[File | DirectoryNoItems])
def search(
    files_system_manager: Annotated[FilesSystemManager, Depends(get_files_system_manager)],
    keyword: str,
    path: str,
    calculate_directories_size: bool = False
):
    items = files_system_manager.search_items_by_keyword(keyword, path)
    return [item_to_pydantic_item_in_list(item, calculate_directories_size) for item in items]


@router.post('/create-default', response_model=DirectoryNoItems)
def create_default(
    files_system_manager: Annotated[FilesSystemManager, Depends(get_files_system_manager)],
    path: str,
):
    parent_directory = files_system_manager.get_directory_from_path(path)
    name = generate_default_directory_name(parent_directory)
    directory = files_system_manager.create_directory(path, name)
    return directory
