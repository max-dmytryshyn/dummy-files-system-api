# Description
This is a pet project of creating a dummy files system with plain Python and wrapping it with FastAPI in order
to provide REST API access to the files system.  
Web frontend - [https://github.com/max-dmytryshyn/dummy-files-system-web](https://github.com/max-dmytryshyn/dummy-files-system-web)  
This project consists of 2 modules: `files_system` independent module with all the business logic implementation of the
files system and `api` which uses `files_system` module for providing consumer with REST API interface.
# Core objects and concepts
### 1. File
`File` is just a plain item with `byte_size` and string `content`  
`File` size must be > 0
### 2. Directory
`Directory` is an item which has dicts of its children (File or Directory) in field `items`.  
It has `byte_size` property which calculates
sum of size of its content
### 3. FilesSystemManager
`FilesSystemManager` is a main class which is responsible for getting/creating/updating/deleting items.  
It also has a `root` folder which is the starting point of system. `root` folder is a `Directory` with no name
### 4. Navigation
All methods of `FilesSystemManager` require path in order to get needed objects.
With the help of path `FilesSystemManager` can easily navigate through `items dicts` of `Directories`.  
Path must start from `/`
### 5. Error handling
Error handling is implemented with custom `exceptions` for every particular case
### 6. Search
- Search is performed by looking into both name and content of file or directory.  
- Search returns all matching items recursively (looking into children folders too) inside selected `Directory`,
`root` by default
### 7. List items with sorting
- By default, returns all items in `item dict` of selected `Directory`, `root` by default
- If `include_inner` is `True` return items recursively
- Sort is supported by `created_at`, `modified_at`, `name`, `byte_size`
- If `calculate_directories_size` is `False` during sorting all `directories` `byte_size` will be considered 0
- Sort by several columns is supported, but only `ASC` or `DESC` for all at once
### 8. Naming
- Name can't be empty
- There can't be items with the same name in the same directory  
- Name can't have any symbols from `['<', '>', ':', '"', '/', '\\', '|', '?', '*']`
