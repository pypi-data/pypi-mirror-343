import sys
import argparse
import sqlite3
import pkg_resources

def main():
    from .remove import remove
    from .rollback import rollback
    
    program = argparse.ArgumentParser(description="Transactional rm command, with power failure protocols")

    program.add_argument("-r", "--rm", help="Remove filesystem items", type=remove, nargs="+")
    program.add_argument("-b", "--rb", help="Rollback previously removed items", type=rollback, nargs="+")

    if len(sys.argv) == 1:
        program.print_help()
        sys.exit(0)

    program.parse_args()

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
    cur.execute("CREATE TABLE IS NOT EXISTS items_rm (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, items TEXT NOT NULL)")

def save(item: str):
    # copies file
    pass

if __name__ == "__main__":
    main()