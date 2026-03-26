from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User
from ..core.security import get_password_hash, verify_password
from ..schemas.schemas import UserCreate, UserOut
from ..exceptions import UserNotFoundError, InvalidCredentialsError
from typing import Optional

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError()
    return user



