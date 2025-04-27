# folder_tree_lister

A small Python package to list the directory tree structure of specified directories. It can display the directory structure up to a certain depth and allows for easy navigation of folder contents. Useful in giving the folder structure as a context to LLMs. 

## Features

- List directory trees for multiple directories.
- Control the depth of directory traversal.
- Exclude unwanted folders like `__pycache__`, `.git`, etc.
- Simple and clean output to visualize folder structures.

## Installation

You can install the package via `pip` from PyPI.



### Install from PyPI:
```bash
pip install folder-tree-lister
```
### Importing the Function:
```bash
from folder_tree_lister import list_multiple_directories

```

### Using the Function:
```bash
import os
dirs = ["."]  
list_multiple_directories(os.getcwd(), dirs, max_depth=4)           

```
#### Add more directories if needed, for eg dirs = [".", "/path/to/other/directory"]. Doing this will create two seperate folder trees.
#### Depth can be addded to set the limit for rendering sub-directories.