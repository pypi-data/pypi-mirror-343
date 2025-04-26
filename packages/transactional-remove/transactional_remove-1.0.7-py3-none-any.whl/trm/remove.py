import shutil
from .utils import *
from os import path, listdir, remove, unlink, rmdir

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
    
