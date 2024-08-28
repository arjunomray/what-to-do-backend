from contextlib import asynccontextmanager
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI

from .internals.auth import get_current_user
from .models.user import User
from .routers import todo, users
from .utils.database import init_db
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


origins = ["http://localhost:5173", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router)
app.include_router(users.router)


@app.get(path="/hello/")
async def index(current_user: Annotated[User, Depends(get_current_user)]):
    return {"message": "welcome to todo api", "user": current_user.username}
