from time import sleep

import pytest

from files_system.manager import FilesSystemManager


@pytest.fixture(scope="function")
def no_init_files_manager():
    return FilesSystemManager()


@pytest.fixture(scope="function")
def get_manager_with_simple_init_files_and_delay():
    """
    Returns function to create manager with the following files:
    /test.txt (test content, 1),
    /folder 1/test2.txt (test content 2, 2)
    and directories:
    /folder 1,
    /folder 1/ folder 2
    and possible delay after that
    """
    def get_manager(delay=0):
        manager = FilesSystemManager()
        manager.create_file('/', 'test.txt', 'test content', 1)
        manager.create_directory('/', 'folder 1')
        manager.create_file('/folder 1', 'test2.txt', 'test content 2', 1)
        manager.create_directory('/folder 1', 'folder 2')
        sleep(delay)
        return manager
    return get_manager


@pytest.fixture(scope="function")
def many_init_files_manager():
    return FilesSystemManager()


@pytest.fixture()
def test_file_data():
    return {
        'name': 'test.txt',
        'content': 'test content',
        'byte_size': 1
    }


@pytest.fixture()
def bad_path_end():
    return '/folder 1/bad file'


@pytest.fixture()
def bad_path_middle():
    return '/test.txt/test.txt'


@pytest.fixture()
def bad_path_no_starting_slash():
    return 'folder 1'
