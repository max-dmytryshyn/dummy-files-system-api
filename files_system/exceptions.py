from files_system.constants import PROHIBITED_NAME_SYMBOLS


class BaseFileSystemException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class DeleteRootDirectoryException(BaseFileSystemException):
    def __init__(self):
        self.message = f"Unable to delete root folder"
        super().__init__(self.message)


class ItemNotFoundException(BaseFileSystemException):
    def __init__(self, path: str):
        self.message = f"No such file or directory: {path}"
        super().__init__(self.message)


class FileNotFoundException(BaseFileSystemException):
    def __init__(self, path: str):
        self.message = f"No such file: {path}"
        super().__init__(self.message)


class DirectoryNotFoundException(BaseFileSystemException):
    def __init__(self, path: str):
        self.message = f"No such directory: {path}"
        super().__init__(self.message)


class ItemAlreadyExistsOnCreateException(BaseFileSystemException):
    def __init__(self, path: str, name: str):
        self.message = f"Unable to create the file or directory at {path}: Item {name} already exists"
        super().__init__(self.message)


class ItemAlreadyExistsOnRenameException(BaseFileSystemException):
    def __init__(self, path: str, name: str):
        self.message = f"Unable to rename the file or directory at {path}: Item {name} already exists"
        super().__init__(self.message)


class EmptyItemNameException(BaseFileSystemException):
    def __init__(self):
        self.message = "Empty name for file or directory is not allowed"
        super().__init__(self.message)


class ProhibitedSymbolInItemNameException(BaseFileSystemException):
    def __init__(self):
        self.message = f"File or directory name can't contain any symbol of {', '.join(PROHIBITED_NAME_SYMBOLS)}"
        super().__init__(self.message)


class NotPositiveFileSizeException(BaseFileSystemException):
    def __init__(self):
        self.message = "File size must be greater than zero"
        super().__init__(self.message)


class NotStartingWithSlashPathException(BaseFileSystemException):
    def __init__(self):
        self.message = "Path must start with / symbol"
        super().__init__(self.message)


class EmptyPathException(BaseFileSystemException):
    def __init__(self):
        self.message = "Path can't be empty"
        super().__init__(self.message)


class SortByThisFieldNotSupported(BaseFileSystemException):
    def __init__(self, field: str):
        self.message = f"Sort by this field is not supported: {field}"
        super().__init__(self.message)


class EmptySearchKeywordException(BaseFileSystemException):
    def __init__(self):
        self.message = "Search keyword can't be empty"
        super().__init__(self.message)
