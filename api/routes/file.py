from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import get_files_system_manager
from api.models.files_system import File, UpdateFileContentRequestBody
from api.utils import generate_default_file_name, generate_default_file_size
from files_system.manager import FilesSystemManager

router = APIRouter(prefix='/file')


@router.put("/update-content", response_model=File)
async def update_content(
    files_system_manager: Annotated[FilesSystemManager, Depends(get_files_system_manager)],
    data: UpdateFileContentRequestBody,
    path: str
):
    return files_system_manager.update_file_content(path, data.content)


@router.post('/create-default', response_model=File)
def create_default(
    files_system_manager: Annotated[FilesSystemManager, Depends(get_files_system_manager)],
    path: str,
):
    parent_directory = files_system_manager.get_directory_from_path(path)
    name = generate_default_file_name(parent_directory)
    size = generate_default_file_size()
    file = files_system_manager.create_file(path, name, '', size)
    return file
