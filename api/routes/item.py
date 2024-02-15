from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import get_files_system_manager
from api.models.files_system import Directory, File, RenameItemRequestBody, DirectoryNoItems
from api.utils import item_to_pydantic_model, item_to_pydantic_item_in_list
from files_system.manager import FilesSystemManager

router = APIRouter(prefix='/item')


@router.get("/get-by-path", response_model=File | Directory)
async def get_by_path(
    files_system_manager: Annotated[FilesSystemManager, Depends(get_files_system_manager)],
    path: str,
    calculate_directories_size: bool = False
):
    item = files_system_manager.get_item_from_path(path)
    return item_to_pydantic_model(item, calculate_directories_size)


@router.put("/rename", response_model=File | DirectoryNoItems)
async def rename(
    files_system_manager: Annotated[FilesSystemManager, Depends(get_files_system_manager)],
    data: RenameItemRequestBody,
    path: str,
    calculate_directories_size: bool = False
):
    item = files_system_manager.rename_item(path, data.name)
    return item_to_pydantic_item_in_list(item, calculate_directories_size)


@router.delete('/delete')
def delete(
    files_system_manager: Annotated[FilesSystemManager, Depends(get_files_system_manager)],
    path: str,
):
    files_system_manager.delete_item(path)
