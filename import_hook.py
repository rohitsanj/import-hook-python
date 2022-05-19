import sqlite3
import importlib.abc

foo_code = """
print("foo is being initialized!")

def add(a, b):
    return a + b

"""

bar_code = """
print("bar is being initialized")

def sub(a, b):
    return a - b

"""

spam_code = """
print("spam is being initialized")

def fib(n: int):
    if n in (0, 1):
        return n

    return fib(n-1) + fib(n-2)
"""


def create_repo_table():
    con = sqlite3.connect(":memory:")
    cursor = con.cursor()
    cursor.execute("create table repository (fullname, source_code)")
    cursor.executemany(
        "insert into repository values (?, ?)",
        [("foo", foo_code), ("bar", bar_code), ("spam", spam_code)],
    )

    con.commit()
    return cursor


class DBFinder(importlib.abc.Finder):
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def find_spec(self, fullname: str, path, target):
        # Query database to see if we have the `fullname` module
        from importlib.machinery import ModuleSpec

        self.cursor.execute("select 1 from repository where fullname = ?", (fullname,))
        if self.cursor.fetchone():
            return ModuleSpec(fullname, DBLoader(cursor=self.cursor))

        # We don't have it in the database, go look elsewhere
        return None


class DBLoader(importlib.abc.Loader):
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self.cursor = cursor

    def exec_module(self, module):
        self.cursor.execute(
            "select source_code from repository where fullname = ?", (module.__name__,)
        )
        source_code = self.cursor.fetchone()
        exec(source_code[0], module.__dict__)


import sys

cursor = create_repo_table()
sys.meta_path.insert(0, DBFinder(cursor=cursor))
