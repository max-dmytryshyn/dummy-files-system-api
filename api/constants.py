from collections import defaultdict
from fastapi import status

from files_system import exceptions


FILES_SYSTEM_EXCEPTIONS_CODE_MAPPING = defaultdict(lambda: status.HTTP_500_INTERNAL_SERVER_ERROR, {
    exceptions.DeleteRootDirectoryException: status.HTTP_400_BAD_REQUEST,
    exceptions.ItemNotFoundException: status.HTTP_404_NOT_FOUND,
    exceptions.FileNotFoundException: status.HTTP_404_NOT_FOUND,
    exceptions.DirectoryNotFoundException: status.HTTP_404_NOT_FOUND,
    exceptions.ItemAlreadyExistsOnCreateException: status.HTTP_400_BAD_REQUEST,
    exceptions.ItemAlreadyExistsOnRenameException: status.HTTP_400_BAD_REQUEST,
    exceptions.EmptyItemNameException: status.HTTP_400_BAD_REQUEST,
    exceptions.ProhibitedSymbolInItemNameException: status.HTTP_400_BAD_REQUEST,
    exceptions.NotPositiveFileSizeException: status.HTTP_400_BAD_REQUEST,
    exceptions.NotStartingWithSlashPathException: status.HTTP_400_BAD_REQUEST,
    exceptions.EmptyPathException: status.HTTP_400_BAD_REQUEST,
    exceptions.SortByThisFieldNotSupported: status.HTTP_400_BAD_REQUEST,
    exceptions.EmptySearchKeywordException: status.HTTP_400_BAD_REQUEST,
})
