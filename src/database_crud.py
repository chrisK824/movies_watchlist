from sqlalchemy.orm import Session
# from sqlalchemy.sql import text
from db_models import Movies
from schemas import Movie, MovieWatch
from datetime import datetime


class TooSoonException(Exception):
    pass


def add_movie(db: Session, movie: Movie):
    db_movie = Movies(title=movie.title, release_date=movie.release_date)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: Session):
    movies = list(db.query(Movies).all())
    return movies

def update_movie(db: Session, movie_id: int, watch: MovieWatch):
    movie_cursor = db.query(Movies).filter(Movies.id == movie_id)
    if not movie_cursor.first():
        raise ValueError(f"There is no movie with ID {movie_id} in the watchlist")

    if watch.value and movie_cursor.first().release_date > datetime.now():
        raise TooSoonException(f"This movie cannot be watched as it isn't released yet!")
    movie_cursor.update(
        {
            Movies.watched: watch.value,
            Movies.watched_date: datetime.now() if watch.value else None
        }
    )
    db.commit()
    return db.query(Movies).filter(Movies.id == movie_id).first()


def get_watched_movies(db: Session):
    return list(db.query(Movies).filter(Movies.watched == True).all())


def get_upcoming_movies(db: Session):
    return list(db.query(Movies).filter(Movies.release_date > datetime.now()).all())


def search_movies(db: Session, keyword: str):
    return list(db.query(Movies).filter(Movies.title.contains(keyword)).all())
