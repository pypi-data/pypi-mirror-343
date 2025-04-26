import shutil
import sqlite3
import pkg_resources
from os import path, listdir, remove, unlink, rmdir

# type constants (file, links, empty directories, and directories with items)
FILE = "file"
DIR = "dir"
LINK = "link"
DIRF = "dirf"

# action constants (true for rollback, false for remove)
RM = False
RB = True

def log(item: str, type: str, action: bool):
    # logs actions
    db_path = pkg_resources.resource_filename("trm", "trm.sql")
    print(db_path)
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items_rm (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, items TEXT NOT NULL)")

def save(item: str):
    # copies file
    pass

def state(item):
    if path.isfile(item):
        return FILE
    elif path.isdir(item):
        if listdir(item) != None:
            return DIRF
        else:
            return DIR
    elif path.islink(item):
        return LINK

def remove(item):
    type = state(item)
    match type:
        case "file": log(item, type, RM); '''save(item); os.remove(item)'''
        case "link": log(item, type, RM); '''save(item); os.unlink(item)'''
        case "dir": log(item, type, RM); '''save(item); os.rmdir(item)'''
        case "dirf": log(item, type, RM); '''save(item); shutil.rmtree(item)'''
        case _: return
    
def rollback(items):
    pass