from sqlalchemy.orm import Session
from db_models import Movie
from schemas import Movie, MovieWatch
from datetime import datetime


class TooSoonException(Exception):
    pass


def add_movie(db: Session, movie: Movie):
    db_movie = Movie(title=movie.title, release_date=movie.release_date)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_movies(db: Session):
    movies = list(db.query(Movie).all())
    return movies


def update_movie(db: Session, movie_id: int, watch: MovieWatch):
    movie_cursor = db.query(Movie).filter(Movie.id == movie_id)
    if not movie_cursor.first():
        raise ValueError(
            f"There is no movie with ID {movie_id} in the watchlist")

    if watch.value and movie_cursor.first().release_date > datetime.now():
        raise TooSoonException(
            f"This movie cannot be watched as it isn't released yet!")
    movie_cursor.update(
        {
            Movie.watched: watch.value,
            Movie.watched_date: datetime.now() if watch.value else None
        }
    )
    db.commit()
    return db.query(Movie).filter(Movie.id == movie_id).first()


def get_watched_movies(db: Session):
    return list(db.query(Movie).filter(Movie.watched == True).all())


def get_upcoming_movies(db: Session):
    return list(db.query(Movie).filter(Movie.release_date > datetime.now()).all())


def search_movies(db: Session, keyword: str):
    return list(db.query(Movie).filter(Movie.title.contains(keyword)).all())
