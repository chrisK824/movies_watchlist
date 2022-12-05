from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db_models import Movie, User, Watchlist
import schemas
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from authentication import get_password_hash, verify_password, oauth2_scheme, get_token_payload, BearAuthException
from database import SessionLocal


class DuplicateError(Exception):
    pass


class TooSoonException(Exception):
    pass


def get_db():
    movies_watchlists_db = SessionLocal()
    try:
        yield movies_watchlists_db
    finally:
        movies_watchlists_db.close()


def add_user(db: Session, user: schemas.UserSignUp):
    user = User(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password),
        name=user.name,
        surname=user.surname,
        country=user.country
    )
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateError(
            f"Email {user.email} is already attached to a registered user. Try to login.")


def get_user(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    return user


def activate_user(db: Session, user: User):
    user = db.query(User).filter(User.email == user.email).first()
    if not user:
        return False
    user.register_activated = True
    db.commit()
    return user


def authenticate_user(db: Session, user_email: str, password: str):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        print("no user")
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        user_email = get_token_payload(token)
    except BearAuthException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate bearer token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


def add_movie(db: Session, movie: schemas.Movie):
    db_movie = Movie(title=movie.title, release_date=movie.release_date,
                     category=movie.category, summary=movie.summary)
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
    movie = db.query(Movie).filter(Movie.id == movie_id).delete()
    if not movie:
        raise ValueError(
            f"There is no movie with ID {movie_id}.")
    else:
        db.commit()


def search_movies(db: Session, keyword: str):
    return list(db.query(Movie).filter(Movie.title.contains(keyword)).all())


def get_upcoming_movies(db: Session):
    return list(db.query(Movie).filter(Movie.release_date > datetime.now()).all())


def add_movie_to_watchlist(db: Session, movie_id: int, user_email: str):
    movie_cursor = db.query(Movie).filter(Movie.id == movie_id)
    if not movie_cursor.first():
        raise ValueError(
            f"There is no movie with ID {movie_id}.")

    user_cursor = db.query(User).filter(User.email == user_email)
    if not user_cursor.first():
        raise ValueError(
            f"There is no user registered with email {user_email}.")

    watchlist_entry = Watchlist(movie_id=movie_id, user_email=user_email)
    try:
        db.add(watchlist_entry)
        db.commit()
    except IntegrityError:
        db.rollback()
        user = user_cursor.first()
        raise DuplicateError(
            f"{user.username} you have already movie {movie_id} in your watchlist.")

    return watchlist_entry


def remove_movie_from_watchlist(db: Session, movie_id: int, user_email: str):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise ValueError(
            f"There is no user registered with email {user_email}.")

    watchlist_entry = db.query(Watchlist).filter(
        Watchlist.movie_id == movie_id).delete()
    if not watchlist_entry:
        raise ValueError(
            f"{user.username}, there is no movie with ID {movie_id} in your watchlist.")
    db.commit()


def get_watchlist_movies(db: Session, user_email: str):
    query = """SELECT * FROM 
    movies JOIN watchlists ON watchlists.movie_id = movies.id 
    WHERE watchlists.user_email = :user_email;"""

    movies = list(db.execute(
        text(query), [{"user_email": user_email}]).fetchall())
    return movies


def get_watchlist_watched_movies(db: Session, user_email: str):
    query = """SELECT * FROM 
    movies JOIN watchlists ON watchlists.movie_id = movies.id 
    WHERE watchlists.user_email = :user_email AND 
    watchlists.watched = True;"""

    movies = list(db.execute(
        text(query), [{"user_email": user_email}]).fetchall())
    return movies


def get_watchlist_upcoming_movies(db: Session, user_email: str):
    query = """SELECT * FROM 
    movies JOIN watchlists ON watchlists.movie_id = movies.id 
    WHERE watchlists.user_email = :user_email 
    AND movies.release_date > datetime(date('now'))
    """

    movies = list(db.execute(
        text(query), [{"user_email": user_email}]).fetchall())
    return movies


def get_watchlist_movie(db: Session, movie_id: int, user_email: str):
    query = """SELECT * FROM 
    movies JOIN watchlists ON watchlists.movie_id = movies.id 
    WHERE watchlists.user_email = :user_email AND 
    movies.id = :movie_id;"""

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise ValueError(
            f"There is no user registered with email {user_email}.")

    movie = db.execute(
        text(query), [{"user_email": user_email, "movie_id": movie_id}]).fetchone()
    if not movie:
        raise ValueError(
            f"{user.username}, there is no movie with ID {movie_id} in your watchlist.")
    return movie


def watch_movie(db: Session, movie_id: int, user_email: str):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise ValueError(
            f"There is no user registered with email {user_email}.")

    watchlist_entry = db.query(Watchlist).filter(
        Watchlist.movie_id == movie_id).first()
    if not watchlist_entry:
        raise ValueError(
            f"{user.username}, there is no movie with ID {movie_id} in your watchlist.")

    movie_release_date = db.query(Movie.release_date).filter(
        Movie.id == movie_id).first()
    if movie_release_date[0] > datetime.now():
        raise TooSoonException(
            f"{user.username} you cannot watch a not released movie, be patient!")

    watchlist_entry.watched = True
    watchlist_entry.watched_date = datetime.now()
    db.commit()

    query = """SELECT * FROM 
    movies JOIN watchlists ON watchlists.movie_id = movies.id 
    WHERE watchlists.user_email = :user_email AND 
    movies.id = :movie_id;"""

    watchlist_entry = db.execute(
        text(query), [{"user_email": user_email, "movie_id": movie_id}]).fetchone()
    return watchlist_entry
