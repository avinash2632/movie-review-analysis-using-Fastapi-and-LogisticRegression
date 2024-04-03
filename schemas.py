from pydantic import BaseModel

class ReviewBase(BaseModel):
    text: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    sentiment: str
    movie_id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    reviews: list[Review] = []

    class Config:
        orm_mode = True
