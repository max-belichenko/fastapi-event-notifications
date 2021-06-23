import datetime
from typing import List, Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    title: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserSettingsBase(BaseModel):
    timezone: str
    is_receive_notifications: bool


class UserSettingsCreate(UserSettingsBase):
    pass


class UserSettings(UserSettingsBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    title: str
    message: str

    send_date: Optional[datetime.date] = None


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    time_created: datetime.datetime
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    # roles: List[Role] = []
    # settings: Optional[UserSettings] = None
    # events: List[Event] = []

    class Config:
        orm_mode = True
