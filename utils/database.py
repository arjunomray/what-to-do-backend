from sqlmodel import SQLModel, create_engine, Session


sqlite_db = "todos.db"
sqlite_url = f"sqlite:///{sqlite_db}"


engine = create_engine(sqlite_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


init_db()
