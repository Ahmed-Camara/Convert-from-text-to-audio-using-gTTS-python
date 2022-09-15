import common
import os
import shutil

def FlushRepository():
    folder = common.PATH_FOLDER
    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)
