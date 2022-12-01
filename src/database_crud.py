from sqlalchemy.orm import Session
from db_models import Movie, User, Watchlist
import schemas
from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class DuplicateError(Exception):
    pass


class TooSoonException(Exception):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def add_user(db: Session, user: schemas.UserSignUp):
    user = User(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password)
    )
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateError(
                f"Email {user.email} is already attached to a registered user. Try to login.")


def add_movie(db: Session, movie: schemas.Movie):
    db_movie = Movie(title=movie.title, release_date=movie.release_date)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_movies(db: Session):
    movies = list(db.query(Movie).all())
    return movies


def get_movie(db: Session, movie_id: int):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise ValueError(
            f"There is no movie with ID {movie_id}.")
    return movie


def delete_movie(db: Session, movie_id: int):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise ValueError(
            f"There is no movie with ID {movie_id}.")
    else:
        db.delete(movie)
        db.commit()


def search_movies(db: Session, keyword: str):
    return list(db.query(Movie).filter(Movie.title.contains(keyword)).all())

def get_upcoming_movies(db: Session):
    return list(db.query(Movie).filter(Movie.release_date > datetime.now()).all())


# def update_movie(db: Session, movie_id: int, watch: MovieWatch):
#     movie_cursor = db.query(Movie).filter(Movie.id == movie_id)
#     if not movie_cursor.first():
#         raise ValueError(
#             f"There is no movie with ID {movie_id} in the watchlist.")

#     if watch.value and movie_cursor.first().release_date > datetime.now():
#         raise TooSoonException(
#             f"This movie cannot be watched as it isn't released yet!")
#     movie_cursor.update(
#         {
#             Movie.watched: watch.value,
#             Movie.watched_date: datetime.now() if watch.value else None
#         }
#     )
#     db.commit()
#     return db.query(Movie).filter(Movie.id == movie_id).first()


# def get_watched_movies(db: Session):
#     return list(db.query(Movie).filter(Movie.watched == True).all())


