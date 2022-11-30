from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class Movie(BaseModel):
    title: str
    release_date: date

class MovieDetails(Movie):
    id: int
    class Config:
        orm_mode = True

class MovieWatch(BaseModel):
    value: bool

class UserSignUp(BaseModel):
    email : str
    username : str
    password : str

class User(UserSignUp):
    register_date : datetime
    register_activated : bool

    class Config:
        orm_mode = True

class Watchlist(Movie):
    movie_id : int
    user_email : str
    added_in_watchlist: datetime
    watched: bool
    watched_date: Optional[datetime] = None

    class Config:
        orm_mode = True
