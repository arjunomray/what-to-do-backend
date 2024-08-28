from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from ..internals.auth import get_current_user
from ..models.user import User
from ..models.todo import Todo, TodoBase
from ..utils.database import get_session
from sqlmodel import select
import random


router = APIRouter(prefix="/todos")


@router.get(path="/{todo_id}")
async def get_one(
    todo_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    with next(get_session()) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Did not found"
            )
        if todo.owner != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid request"
            )
        return todo


@router.get(path="/")
async def get_all(
    current_user: Annotated[User, Depends(get_current_user)],
) -> List[Todo]:
    with next(get_session()) as session:
        todo_list = session.exec(
            select(Todo).where(Todo.owner == current_user.username)
        ).all()
        print(current_user.username)
    return todo_list


@router.post(path="/create")
async def create_one(
    todo: TodoBase,
    current_user: Annotated[User, Depends(get_current_user)],
):
    todo = Todo(
        name=todo.name,
        is_complete=False,
        id=random.randint(10000, 1000000),
        owner=current_user.username,
    )
    with next(get_session()) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
    return todo


@router.patch("/update_state/{todo_id}", response_model=Todo)
async def update_state(
    todo_id: int, todo: Todo,  current_user: Annotated[User, Depends(get_current_user)]
):
    with next(get_session()) as session:
        stored_todo = session.get(Todo, todo_id)
        if not stored_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        if stored_todo.owner != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Request"
            )
        stored_todo.is_complete = todo.is_complete
        stored_todo.name = todo.name

        session.add(stored_todo)
        session.commit()
        session.refresh(stored_todo)

        return stored_todo


@router.delete(path="/delete/{todo_id}")
async def delete_one(
    todo_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    with next(get_session()) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        if todo.owner != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Request"
            )
        session.delete(todo)
        session.commit()
        return {"message": f"{todo.name} is deleted"}
