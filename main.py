# main.py

import joblib
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

MODEL_PATH = './sentiment_model/joblib.dump'
sentiment_model = joblib.load(MODEL_PATH)

def analyze_sentiment(review_text: str) -> str:
    prediction = sentiment_model.predict([review_text])
    return 'positive' if prediction[0] == 1 else 'negative'

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_title(db, title=movie.title)
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie already registered")
    return crud.create_movie(db=db, movie=movie)

@app.post("/reviews/{movie_id}", response_model=schemas.Review)
def create_review_for_movie(
    movie_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(review.text)
    return crud.create_review(db=db, review=review, movie_id=movie_id, sentiment=sentiment)

@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies
