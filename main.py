"""Main function."""
from environs import Env

from sqlitedb.sqlite import SQLiteDatabase

env = Env()
env.read_env()
db = SQLiteDatabase()
if __name__ == "__main__":
    print("Hello👋")
