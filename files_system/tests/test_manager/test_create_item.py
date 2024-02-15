import pytest

from files_system.constants import PROHIBITED_NAME_SYMBOLS
from files_system.data_classes import File, Directory
from files_system.manager import FilesSystemManager
from files_system.exceptions import EmptyPathException, EmptyItemNameException, ProhibitedSymbolInItemNameException, \
    NotStartingWithSlashPathException, NotPositiveFileSizeException, ItemAlreadyExistsOnCreateException, \
    ItemNotFoundException


def check_item_after_create(
    item: File | Directory,
    parent_path: str,
    name: str,
    manager: FilesSystemManager,
):
    stripped_parent_path = parent_path.rstrip('/')
    assert item.name == name
    assert item.absolute_path == f"{stripped_parent_path}/{name}"
    assert item.parent_directory.absolute_path == stripped_parent_path if stripped_parent_path else '/'
    assert manager.get_item_from_path(item.absolute_path) == item
    current_parent = item.parent_directory
    while current_parent is not None:
        assert current_parent.modified_at == item.created_at
        current_parent = current_parent.parent_directory


def check_file_after_create(
    file: File,
    parent_path: str,
    name: str,
    byte_size: int,
    content: str,
    manager: FilesSystemManager
):
    check_item_after_create(file, parent_path, name, manager)
    assert file.content == content
    assert file.byte_size == byte_size


def test_create_file(no_init_files_manager, test_file_data):
    manager = no_init_files_manager
    parent_path = '/'
    new_file = manager.create_file(parent_path, **test_file_data)
    check_file_after_create(file=new_file, parent_path=parent_path, manager=manager, **test_file_data)


def test_create_file_in_directory(get_manager_with_simple_init_files_and_delay, test_file_data):
    manager = get_manager_with_simple_init_files_and_delay(delay=0.5)
    parent_path = '/folder 1'
    new_file = manager.create_file(parent_path, **test_file_data)
    check_file_after_create(file=new_file, parent_path=parent_path, manager=manager, **test_file_data)


def test_create_file_in_directory_trailing_slash(get_manager_with_simple_init_files_and_delay, test_file_data):
    manager = get_manager_with_simple_init_files_and_delay(delay=0.5)
    parent_path = '/folder 1/'
    new_file = manager.create_file(parent_path, **test_file_data)
    check_file_after_create(file=new_file, parent_path=parent_path, manager=manager, **test_file_data)


def test_create_directory(no_init_files_manager):
    manager = no_init_files_manager
    parent_path = '/'
    name = 'folder'
    new_directory = manager.create_directory(parent_path, 'folder')
    check_item_after_create(item=new_directory, parent_path=parent_path, manager=manager, name=name)


def test_create_directory_in_directory(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay(delay=0.5)
    parent_path = '/folder 1'
    name = 'folder'
    new_directory = manager.create_directory(parent_path, 'folder')
    check_item_after_create(item=new_directory, parent_path=parent_path, manager=manager, name=name)


def test_create_directory_in_directory_trailing_slash(get_manager_with_simple_init_files_and_delay, test_file_data):
    manager = get_manager_with_simple_init_files_and_delay(delay=0.5)
    parent_path = '/folder 1/'
    name = 'folder'
    new_directory = manager.create_directory(parent_path, 'folder')
    check_item_after_create(item=new_directory, parent_path=parent_path, manager=manager, name=name)


def test_create_file_already_exists(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemAlreadyExistsOnCreateException):
        manager.create_file('/', 'test.txt', '', 123)


def test_create_file_bad_path_end(get_manager_with_simple_init_files_and_delay, bad_path_end):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.create_file(bad_path_end, 'test.txt', '', 123)


def test_create_file_bad_path_middle(get_manager_with_simple_init_files_and_delay, bad_path_middle):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.create_file(bad_path_middle, 'test.txt', '', 123)


def test_create_file_bad_path_no_starting_slash(
    get_manager_with_simple_init_files_and_delay,
    bad_path_no_starting_slash
):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(NotStartingWithSlashPathException):
        manager.create_file(bad_path_no_starting_slash, 'test.txt', '', 123)


def test_create_file_empy_path(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(EmptyPathException):
        manager.create_file('', "test.txt", "", 1)


def test_create_file_no_starting_slash_path(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(NotStartingWithSlashPathException):
        manager.create_file('folder 1/', "test.txt", "", 1)


def test_create_file_empty_name(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(EmptyItemNameException):
        manager.create_file('/', "", "", 1)


def test_create_file_prohibited_name(no_init_files_manager):
    manager = no_init_files_manager
    for prohibited_symbol in PROHIBITED_NAME_SYMBOLS:
        with pytest.raises(ProhibitedSymbolInItemNameException):
            manager.create_file('/', f'test{prohibited_symbol}', '', 123)


def test_create_file_zero_size(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(NotPositiveFileSizeException):
        manager.create_file('/', 'trest.txt', '', 0)


def test_create_file_negative_size(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(NotPositiveFileSizeException):
        manager.create_file('/', 'trest.txt', '', -1)


def test_create_directory_already_exists(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemAlreadyExistsOnCreateException):
        manager.create_directory('/', 'folder 1')


def test_create_directory_bad_path_end(get_manager_with_simple_init_files_and_delay, bad_path_end):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.create_directory(bad_path_end, 'folder')


def test_create_directory_bad_path_middle(get_manager_with_simple_init_files_and_delay, bad_path_middle):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.create_directory(bad_path_middle, 'folder')


def test_create_directory_bad_path_no_starting_slash(
    get_manager_with_simple_init_files_and_delay,
    bad_path_no_starting_slash
):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(NotStartingWithSlashPathException):
        manager.create_directory(bad_path_no_starting_slash, 'folder')


def test_create_directory_empy_path(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(EmptyPathException):
        manager.create_directory('', "folder")


def test_create_directory_no_starting_slash_path(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(NotStartingWithSlashPathException):
        manager.create_directory('folder 1/', "folder")


def test_create_directory_empty_name(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(EmptyItemNameException):
        manager.create_directory('/', "")


def test_create_directory_prohibited_name(no_init_files_manager):
    manager = no_init_files_manager
    for prohibited_symbol in PROHIBITED_NAME_SYMBOLS:
        with pytest.raises(ProhibitedSymbolInItemNameException):
            manager.create_directory('/', f'folder{prohibited_symbol}')
