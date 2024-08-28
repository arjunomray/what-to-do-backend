from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os
load_dotenv()


sqlite_db = "todos.db"
sqlite_url = os.getenv('DB_STRING')


engine = create_engine(sqlite_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


init_db()
