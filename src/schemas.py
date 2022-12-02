from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class Movie(BaseModel):
    title: str
    release_date: date
    category: str
    summary: str


class MovieDetails(Movie):
    id: int

    class Config:
        orm_mode = True


class UserSignUp(BaseModel):
    email: str
    username: str
    password: str
    name: str
    surname : str
    country : str


class User(UserSignUp):
    register_date: datetime
    register_activated: bool

    class Config:
        orm_mode = True


class WatchlistInput(BaseModel):
    movie_id: int


class Watchlist(WatchlistInput):
    added_in_watchlist: datetime
    watched: bool
    watched_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class WatchlistMovie(BaseModel):
    title: str
    release_date: datetime
    movie_id: int
    added_in_watchlist: datetime
    watched: bool
    watched_date: Optional[datetime] = None


class Token(BaseModel):
    access_token : str
    token_type : str