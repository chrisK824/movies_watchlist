from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class Movie(BaseModel):
    title: str
    release_date : date
    class Config:
        orm_mode = True

class MovieDetails(Movie):
    id : int
    added_in_watchlist : datetime
    watched : bool
    watched_date : Optional[datetime] = None
    class Config:
        orm_mode = True

class MovieWatch(BaseModel):
    value : bool
    class Config:
        orm_mode = True

