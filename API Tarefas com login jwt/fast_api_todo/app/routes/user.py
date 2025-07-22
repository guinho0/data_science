from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm

from app.models import User
from app.schemas import UserCreate, UserRead, Token
from app.auth import get_session, hash_password, verify_password, create_access_token

router = APIRouter(tags=["Usuários"])

@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.username == user_data.username)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Usuário já existe.")

    hashed_pwd = hash_password(user_data.password)
    new_user = User(username=user_data.username, password=hashed_pwd)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
