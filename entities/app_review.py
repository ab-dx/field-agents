from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

from entities.base import RawReview


class CustomerReview(RawReview):
    csat_score: int = Field(ge=1, le=5, description="Customer satisfaction 1-5")
    nps_score: int = Field(ge=0, le=10, description="Net Promoter Score 0-10")

class EmployeeReview(RawReview):
    esat_score: int = Field(ge=1, le=5, description="1-5★ Employee satisfaction") 
    enps_score: int = Field(ge=-100, le=100, description="Employee Net Promoter Score")
    recommend_score: int = Field(ge=0, le=10, description="0-10 Recommend to colleague")

class GlassdoorEmployeeReview(EmployeeReview):
    platform: Literal["glassdoor"] = "glassdoor"
    star_rating: Optional[float] = Field(ge=1, le=5)
    pros: Optional[List[str]] = []
    cons: Optional[List[str]] = []
    likes: Optional[int] = Field(None, ge=0)

class GlassdoorEmployeeSalary(EmployeeReview):
    platform: Literal["glassdoor"] = "glassdoor"
    post: Optional[str] = None
    base_salary: Optional[int] = Field(None, ge=0)
    star_rating: Optional[float] = Field(ge=1, le=5)
    jobs: Optional[int] = Field(None, ge=0)

class GlassdoorEmployeeBenifit(EmployeeReview):
    platform: Literal["glassdoor"] = "glassdoor"
    benifit: Optional[str] = None
    star_rating: Optional[float] = Field(ge=1, le=5)
    likes: Optional[int] = Field(None, ge=0)
    
    
class GlassdoorEmployeeReviewList(BaseModel):
    comp_name: Optional[str] = None
    no_of_reviews: Optional[int] = Field(None, ge=0)
    overall_star_rating: Optional[float] = Field(ge=1, le=5)
    recommend_to_friend_pct: Optional[float] = Field(ge=0, le=100)
    ceo_approval_pct: Optional[float] = Field(ge=0, le=100)
    reviews: List[GlassdoorEmployeeReview] = []
    salaries: List[GlassdoorEmployeeSalary] = []
    benifits: List[GlassdoorEmployeeBenifit] = []
    
class RedditCustomerReview(CustomerReview):
    platform: Literal["reddit"] = "reddit"
    upvotes: Optional[int] = Field(None, ge=0)


class PlayStoreCustomerReview(CustomerReview):
    platform: Literal["playstore"] = "playstore"
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
    app_name: Optional[str] = None
    no_of_reviews: Optional[int] = Field(None, ge=0)
    no_of_downloads: Optional[int] = Field(None, ge=0)
    avg_star_rating: Optional[float] = Field(None, ge=1, le=5)
    reviews: List[PlayStoreCustomerReview]


class XReviewList(BaseModel):
    reviews: List[XCustomerReview]
