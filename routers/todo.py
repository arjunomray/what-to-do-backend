from typing import List
from fastapi import APIRouter, HTTPException
from ..models.todo import Todo, TodoBase
from ..utils.database import get_session
from sqlmodel import select
import random


router = APIRouter(prefix="/items")


@router.get(path="/{todo_id}")
async def get_one(todo_id: int):
    with next(get_session()) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return HTTPException(status_code=404, detail="Did not found")
        return todo


@router.get(path="/")
async def get_all() -> List[Todo]:
    with next(get_session()) as session:
        todo_list = session.exec(select(Todo)).all()
    return todo_list


@router.post(path="/create")
async def create_one(todo: TodoBase):
    todo = Todo(
        name=todo.name, is_complete=todo.is_complete, id=random.randint(10000, 1000000)
    )
    with next(get_session()) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
    return todo


@router.delete(path="/delete/{todo_id}")
async def delete_one(todo_id: int):
    with next(get_session()) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"message": f"{todo.name} is deleted"}

