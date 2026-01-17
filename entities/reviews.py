from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum

class RawReview(BaseModel):
    review_text: str = Field(min_length=1, max_length=10000)
    review_title: Optional[str] = None
    star_rating: float = Field(ge=1, le=5)

class RawReviewList(BaseModel):
    positive_reviews: List[RawReview] = Field(description="positive reviews")
    negative_reviews: List[RawReview] = Field(description="negative reviews")
