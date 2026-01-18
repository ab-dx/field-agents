from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

from entities.base import RawReview


class CustomerReview(RawReview):
    csat_score: int = Field(ge=1, le=5, description="Customer satisfaction 1-5")
    nps_score: int = Field(ge=0, le=10, description="Net Promoter Score 0-10")


class RedditCustomerReview(CustomerReview):
    platform: Literal["reddit"] = "reddit"
    upvotes: Optional[int] = Field(None, ge=0)


class PlayStoreCustomerReview(CustomerReview):
    platform: Literal["playstore"] = "playstore"
    no_of_reviews: Optional[int] = Field(None, ge=0)
    no_of_downloads: Optional[int] = Field(None, ge=0)
    star_rating: float = Field(ge=1, le=5)
    created_at: Optional[datetime] = None


class XCustomerReview(CustomerReview):
    platform: Literal["x"] = "x"
    likes: Optional[int] = Field(None, ge=0)
    reposts: Optional[int] = Field(None, ge=0)
    replies: Optional[int] = Field(None, ge=0)


class RedditReviewList(BaseModel):
    reviews: List[RedditCustomerReview]


class PlayStoreReviewList(BaseModel):
    reviews: List[PlayStoreCustomerReview]


class XReviewList(BaseModel):
    reviews: List[XCustomerReview]
