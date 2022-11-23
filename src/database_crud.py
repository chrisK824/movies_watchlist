from sqlalchemy.orm import Session
# from sqlalchemy.sql import text
import db_models
import schemas


def get_movies(db: Session):
    movies = []
    movies = list(db.query(db_models.Movie).all())
    return movies


def add_movie(db: Session, movie: schemas.Movie):
    db_movie = db_models.Movie(title = movie.title, release_date=movie.release_date)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
