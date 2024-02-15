import pytest
from files_system.utils import get_items_names_from_path, is_directory, is_file
from files_system.exceptions import EmptyPathException, NotStartingWithSlashPathException
from files_system.data_classes import File, Directory


@pytest.fixture
def file_no_parent():
    return File(name='test.txt', content='content', byte_size=12341)


@pytest.fixture
def directory_no_parent_no_items():
    return Directory(name='test.txt')


def test_get_items_names_from_path_root():
    assert get_items_names_from_path('/') == []


def test_get_items_names_from_path_item_no_trailing_slash():
    assert get_items_names_from_path('/folder') == ['folder']


def test_get_items_names_from_path_item_trailing_slash():
    assert get_items_names_from_path('/folder/') == ['folder']


def test_get_items_names_from_path_multiple_items_no_trailing_slash():
    assert get_items_names_from_path('/folder/test.txt') == ['folder', 'test.txt']


def test_get_items_names_from_path_multiple_items_trailing_slash():
    assert get_items_names_from_path('/folder/test.txt/') == ['folder', 'test.txt']


def test_get_items_names_from_path_empty_path():
    with pytest.raises(EmptyPathException):
        get_items_names_from_path('')


def test_get_items_names_from_path_item_no_starting_slash_no_trailing_slash():
    with pytest.raises(NotStartingWithSlashPathException):
        get_items_names_from_path('folder')


def test_get_items_names_from_path_item_no_starting_slash_trailing_slash():
    with pytest.raises(NotStartingWithSlashPathException):
        get_items_names_from_path('folder/')


def test_get_items_names_from_path_multiple_items_no_starting_slash_no_trailing_slash():
    with pytest.raises(NotStartingWithSlashPathException):
        get_items_names_from_path('folder/test.txt')


def test_get_items_names_from_path_multiple_items_no_starting_slash_trailing_slash():
    with pytest.raises(NotStartingWithSlashPathException):
        get_items_names_from_path('folder/test.txt/')


def test_is_directory_with_directory(directory_no_parent_no_items):
    assert is_directory(directory_no_parent_no_items)


def test_is_directory_with_file(file_no_parent):
    assert not is_directory(file_no_parent)


def test_is_file_with_directory(directory_no_parent_no_items):
    assert not is_file(directory_no_parent_no_items)


def test_is_file_with_file(file_no_parent):
    assert is_file(file_no_parent)
