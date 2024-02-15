import pytest
from files_system.exceptions import DirectoryNotFoundException, FileNotFoundException, ItemNotFoundException, \
    NotStartingWithSlashPathException, EmptyPathException


def test_get_item_from_path_root(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/')
    assert item == manager.root


def test_get_item_from_path_file(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/test.txt')
    assert item == manager.root.items['test.txt']


def test_get_item_from_path_file_trailing_slash(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/test.txt/')
    assert item == manager.root.items['test.txt']


def test_get_item_from_path_file_in_directory(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/folder 1/test2.txt')
    assert item == manager.root.items['folder 1'].items['test2.txt']


def test_get_item_from_path_file_in_directory_trailing_slash(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/folder 1/test2.txt/')
    assert item == manager.root.items['folder 1'].items['test2.txt']


def test_get_item_from_path_directory(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/folder 1')
    assert item == manager.root.items['folder 1']


def test_get_item_from_path_directory_trailing_slash(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/folder 1/')
    assert item == manager.root.items['folder 1']


def test_get_item_from_path_directory_in_directory(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/folder 1/folder 2')
    assert item == manager.root.items['folder 1'].items['folder 2']


def test_get_item_from_path_directory_in_directory_trailing_slash(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_item_from_path('/folder 1/folder 2/')
    assert item == manager.root.items['folder 1'].items['folder 2']


def test_get_item_from_path_bad_path_end(get_manager_with_simple_init_files_and_delay, bad_path_end):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.get_item_from_path(bad_path_end)


def test_get_item_from_path_bad_path_middle(get_manager_with_simple_init_files_and_delay, bad_path_middle):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.get_item_from_path(bad_path_middle)


def test_get_item_from_path_bad_path_no_starting_slash(
    get_manager_with_simple_init_files_and_delay,
    bad_path_no_starting_slash
):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(NotStartingWithSlashPathException):
        manager.get_item_from_path(bad_path_no_starting_slash)


def test_get_item_from_path_no_path(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(EmptyPathException):
        manager.get_item_from_path('')


def test_get_file_from_path_file(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_file_from_path('/folder 1/test2.txt')
    assert item == manager.root.items['folder 1'].items['test2.txt']


def test_get_file_from_path_directory(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(FileNotFoundException):
        manager.get_file_from_path('/folder 1/folder 2/')


def test_get_file_from_path_bad_path_end(get_manager_with_simple_init_files_and_delay, bad_path_end):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.get_file_from_path(bad_path_end)


def test_get_file_from_path_bad_path_middle(get_manager_with_simple_init_files_and_delay, bad_path_middle):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.get_file_from_path(bad_path_middle)


def test_get_file_from_path_bad_path_no_starting_slash(
    get_manager_with_simple_init_files_and_delay,
    bad_path_no_starting_slash
):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(NotStartingWithSlashPathException):
        manager.get_file_from_path(bad_path_no_starting_slash)


def test_get_file_from_path_no_path(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(EmptyPathException):
        manager.get_file_from_path('')


def test_get_directory_from_path_directory(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    item = manager.get_directory_from_path('/folder 1/folder 2/')
    assert item == manager.root.items['folder 1'].items['folder 2']


def test_get_directory_from_path_file(get_manager_with_simple_init_files_and_delay):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(DirectoryNotFoundException):
        manager.get_directory_from_path('/folder 1/test2.txt/')


def test_get_directory_from_path_bad_path_end(get_manager_with_simple_init_files_and_delay, bad_path_end):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.get_directory_from_path(bad_path_end)


def test_get_directory_from_path_bad_path_middle(get_manager_with_simple_init_files_and_delay, bad_path_middle):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(ItemNotFoundException):
        manager.get_directory_from_path(bad_path_middle)


def test_get_directory_from_path_bad_path_no_starting_slash(
    get_manager_with_simple_init_files_and_delay,
    bad_path_no_starting_slash
):
    manager = get_manager_with_simple_init_files_and_delay()
    with pytest.raises(NotStartingWithSlashPathException):
        manager.get_directory_from_path(bad_path_no_starting_slash)


def test_get_directory_from_path_no_path(no_init_files_manager):
    manager = no_init_files_manager
    with pytest.raises(EmptyPathException):
        manager.get_directory_from_path('')
