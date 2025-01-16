import os
from sqlalchemy import create_engine

def my_engine():
    DATABASE_URL = os.getenv("DATABASE_URL")
    print("CONN STRING TO DB:",DATABASE_URL)
    return create_engine(DATABASE_URL)