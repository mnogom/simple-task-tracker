from fastapi import APIRouter

from app.api.api_v1.endpoints import tasks, users, login

api_router = APIRouter()
api_router.include_router(login.router, prefix='', tags=['jwt-auth'])
api_router.include_router(tasks.router, prefix='/tasks', tags=['tasks'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
