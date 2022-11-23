from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime

class Movie(BaseModel):
    title: str
    release_date : datetime
    class Config:
        orm_mode = True

class MovieDetails(Movie):
    id : int
    title: str
    release_date : datetime
    added_in_watchlist : datetime
    watched : bool
    watched_date : datetime
    class Config:
        orm_mode = True

