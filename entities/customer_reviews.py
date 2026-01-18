from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Literal
from entities.base import RawReview 
from statistics import mean
from datetime import datetime

class CustomerReview(RawReview):
    csat_score: int = Field(ge=1, le=5, description="Customer satisfaction 1-5")
    nps_score: int = Field(ge=0, le=10, description="Net Promoter Score 0-10")

class CustomerReviewList(BaseModel):
    reviews: List[CustomerReview]

class CustomerReviewReport(BaseModel):
    reviews: List[CustomerReview]
    computed_at: datetime = datetime.now()

    @computed_field
    def sentiment_score(self) -> float:
        return mean(r.llm_content.sentiment_score for r in self.reviews)

    @computed_field
    def avg_csat(self) -> float:
        return mean(r.csat_score for r in self.reviews)

    @computed_field
    def avg_nps(self) -> float:
        return mean(r.nps_score for r in self.reviews)

    @computed_field
    def data_quality(self) -> float:
        avg_conf = mean(r.llm_content.extraction_confidence for r in self.reviews)
        completeness = min(len(self.reviews) / 5, 1.0)
        return (avg_conf * 0.7) + (completeness * 0.3)

