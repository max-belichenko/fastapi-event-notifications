from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas


def get_password_hash(password: str):
    """
    Хэширует полученный парол и возвращает хэш пароля.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(title=role.title, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_role_by_title(db: Session, title: str):
    return db.query(models.Role).filter(models.Role.title == title).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()


def set_user_role(db: Session, user_id: int, role_id: int):
    """
    Добавляет Пользователю указанную Роль.
    """
    db_user = db.query(models.User).get(user_id)
    db_role = db.query(models.Role).get(role_id)

    if db_user and db_role:
        db_user.roles.append(db_role)
        db.commit()
        db.refresh(db_user)

    return db_user


def remove_user_role(db: Session, user_id: int, role_id: int):
    """
    Удаляет у Пользователя указанную Роль.
    """
    db_user = db.query(models.User).get(user_id)
    db_role = db.query(models.Role).get(role_id)

    if db_user and db_role:
        db_user.roles.remove(db_role)
        db.commit()
        db.refresh(db_user)

    return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
