from files_system.manager import FilesSystemManager

files_system_manager = FilesSystemManager()


def add_init_items(manager):
    manager.create_directory('/', 'folder 1')
    manager.create_directory('/folder 1', 'folder2')
    manager.create_file('/folder 1', 'test.txt', "content", 123)
    manager.create_file('/', 'test2.txt', "content", 123)
    manager.create_file('/', 'test1.txt', "content", 230)


add_init_items(files_system_manager)


async def get_files_system_manager():
    return files_system_manager
