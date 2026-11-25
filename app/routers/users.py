from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..models import User
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(
        email=str(payload.email).lower()
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email address is already registered")
    try:
        return crud.create_user(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email address is already registered")

@router.get("", response_model=list[schemas.UserRead])
def list_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100),
               db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schemas.UserRead)
def edit_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not payload.model_dump(exclude_unset=True, exclude_none=True):
        raise HTTPException(status_code=422, detail="Provide at least one field to update")
    try:
        return crud.update_user(db, user, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email address is already registered")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user)
