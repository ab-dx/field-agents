from pydantic import BaseModel, Field, computed_field
from typing import List, Union
from statistics import mean
from datetime import datetime

from entities.app_review import (RedditCustomerReview,PlayStoreCustomerReview,XCustomerReview,)

AnyCustomerReview = Union[RedditCustomerReview, PlayStoreCustomerReview, XCustomerReview]

class CustomerReviewReport(BaseModel):
    reviews: List[AnyCustomerReview]
    computed_at: datetime = Field(default_factory=datetime.now)

    @computed_field
    def sentiment_score(self) -> float:
        return mean(r.llm_content.sentiment_score for r in self.reviews)

    @computed_field
    def avg_csat(self) -> float:
        return mean(r.csat_score for r in self.reviews)

    @computed_field
    def avg_nps_rating(self) -> float:
        if not self.reviews:
            return 0.0
        return round(mean(r.nps_score for r in self.reviews), 2)

    @computed_field
    def nps(self) -> float:
        if not self.reviews:
            return 0.0

        ratings = [int(r.nps_score) for r in self.reviews]
        total = len(ratings)

        promoters = sum(1 for x in ratings if x >= 9)
        detractors = sum(1 for x in ratings if x <= 6)

        return round(((promoters / total) - (detractors / total)) * 100, 2)

    @computed_field
    def data_quality(self) -> float:
        avg_conf = mean(r.llm_content.extraction_confidence for r in self.reviews)
        completeness = min(len(self.reviews) / 5, 1.0)
        return (avg_conf * 0.7) + (completeness * 0.3)

