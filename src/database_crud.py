from sqlalchemy.orm import Session
# from sqlalchemy.sql import text
from db_models import Movies
from schemas import Movie, MovieWatch
from datetime import datetime

def add_movie(db: Session, movie: Movie):
    db_movie = Movies(title = movie.title, release_date=movie.release_date)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: Session):
    movies = list(db.query(Movies).all())
    return movies

def get_movie(db: Session, movie_id : int):
    return db.query(Movies).filter(Movies.id == movie_id).first()

def update_movie(db: Session, movie_id : int, watch : MovieWatch):
    db_movie = db.query(Movies).filter(Movies.id == movie_id).update( 
        {
            Movies.watched : watch.value,
            Movies.watched_date : datetime.now() if watch.value else None
        }
    )
    db.commit()
    return db.query(Movies).filter(Movies.id == movie_id).first()

def get_watched_movies(db: Session):
    return list(db.query(Movies).filter(Movies.watched == True).all())