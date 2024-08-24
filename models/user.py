from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    email: str | None = Field()
    hashed_password: str = Field()
