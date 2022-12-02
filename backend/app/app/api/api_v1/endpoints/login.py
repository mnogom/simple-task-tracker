from typing import Any
from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, schemas
from app.api import deps
from app.core import security

router = APIRouter()


@router.post('/login/access-token/', response_model=schemas.Token)
def login_access_token(db: Session = Depends(deps.get_db),
                       form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    db_user = crud.authenticate_user(db=db,
                                     email=form_data.username,
                                     password=form_data.password)
    if not db_user:
        raise HTTPException(status_code=400, detail='Incorrect user or password')
    if db_user.is_active == False:
        raise HTTPException(status_code=400, detail='Inactive user')
    access_token = security.create_access_token(subject=db_user.id)
    return {'access_token': access_token,
            'token_type': 'bearer'}


@router.post('/login/test-token/')
def test_token():
    pass


@router.post('/password-recovery/{email}/')
def recovery_password(email):
    pass


@router.post('/reset-password/')
def reset_password():
    pass
