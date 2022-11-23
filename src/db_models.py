from sqlalchemy import Column, DateTime, Integer, String, BOOLEAN
from sqlalchemy.sql import func
from database import Base

class Movie(Base):
    __tablename__ = "movies"
    # autoincreament id for each movie insertion
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    release_date = Column(DateTime)
    added_in_watchlist = Column(DateTime, default=func.now())
    watched = Column(BOOLEAN, default=False)
    watched_date = Column(DateTime, default=func.now())

