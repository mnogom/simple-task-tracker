from fastapi import APIRouter

router = APIRouter()


@router.post('/login/access-token')
def login_access_token():
    pass


@router.post('/login/test-token')
def test_token():
    pass


@router.post('/password-recovery/{email}')
def recovery_password(email):
    pass


@router.post('/reset-password')
def reset_password():
    pass
