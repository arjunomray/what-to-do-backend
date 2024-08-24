from pydantic import BaseModel


class Todo(BaseModel):
    name: str
    is_complete: bool | None = None
