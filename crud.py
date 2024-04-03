

from sqlalchemy.orm import Session
from . import models, schemas

def get_movie_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title == title).first()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(title=movie.title)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def create_review(db: Session, review: schemas.ReviewCreate, movie_id: int, sentiment: str):
    db_review = models.Review(**review.dict(), sentiment=sentiment, movie_id=movie_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def get_reviews_for_movie(db: Session, movie_id: int):
    return db.query(models.Review).filter(models.Review.movie_id == movie_id).all()

