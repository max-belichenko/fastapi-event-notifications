from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


user_roles_table = Table(
    'association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    roles = relationship("Role", secondary=user_roles_table, back_populates="users")
    settings = relationship("UserSettings", uselist=False, back_populates="user")
    events = relationship("Event", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)

    users = relationship(
        "User",
        secondary=user_roles_table,
        back_populates="roles"
    )


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="settings")

    timezone = Column(String, default="Europe/Moscow")
    is_receive_notifications = Column(Boolean, default=True)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship("User", back_populates="events")

    title = Column(String)
    message = Column(Text)

    send_date = Column(Date, server_default=func.current_date())
