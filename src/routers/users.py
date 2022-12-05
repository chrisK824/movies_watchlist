import sys
sys.path.append("..")

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import authentication as auth
import database_crud as db_crud
from schemas import UserSignUp, Token

router = APIRouter(prefix="/v1")


@router.post("/signup", summary="Register a user", tags=["Users"])
def create_user(user: UserSignUp, db: Session = Depends(db_crud.get_db)):
    """
    Registers a user.
    """
    try:
        db_crud.add_user(db, user)
        # TODO : actually send a verification email
        return {
            "resut": "You have successfully signed up. A verification email has been sent to your email address with a link to activate your acount."
        }
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.post("/token", response_model=Token, summary="Login as a user", tags=["Users"])
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_crud.get_db)):
    """
    Logs in a user.
    """
    user = db_crud.authenticate_user(
        db=db, user_email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid user email or passord.")
    try:
        access_token = auth.create_access_token(data=user.email)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")
