from sqlmodel import SQLModel, Field

class TodoBase(SQLModel):
    name: str = Field(index=True)


class Todo(TodoBase, table=True):
    id: int = Field(primary_key=True)
    is_complete: bool = Field(default=False)
