from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, UserUpdate
from .security import hash_password

def create_user(db: Session, payload: UserCreate) -> User:
    user = User(
        full_name=payload.full_name,
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        phone_number=payload.phone_number,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.get(User, user_id)

def get_users(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(User).order_by(User.id).offset(skip).limit(limit)
    return list(db.scalars(stmt))

def update_user(db: Session, user: User, payload: UserUpdate):
    for key, value in payload.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(user, key, str(value).lower() if key == "email" else value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
