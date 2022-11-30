from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = "movies"
    # autoincreament id for each movie insertion
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    release_date = Column(DateTime)

    watchlist = relationship("Watchlist", back_populates="movie")

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    register_date = Column(DateTime, default=func.now())
    register_activated = Column(Boolean, default=False)

    watchlist = relationship("Watchlist", back_populates="user")

class Watchlist(Base):
    __tablename__ = "watchlists"
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_email = Column(String, ForeignKey("users.email"))
    __table_args__ = (
        PrimaryKeyConstraint("movie_id", "user_email", name="user_email_movie")
    )
    added_in_watchlist = Column(DateTime, default=func.now())
    watched = Column(Boolean, default=False)
    watched_date = Column(DateTime)

    movie = relationship("Movie", back_populates="watchlist")
    user = relationship("User", back_populates="watchlist")
