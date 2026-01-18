from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from entities.base import RawReview, RawReviewList, LLMExtractedContent
from statistics import mean

class CustomerReview(RawReview):
    star_rating: float = Field(ge=1, le=5)
    csat_score: int = Field(ge=1, le=5, description="Customer satisfaction 1-5")
    nps_score: int = Field(ge=0, le=10, description="Net Promoter Score 0-10")

class CustomerReviewList(RawReviewList):
    avg_csat: float = Field(ge=1, le=5)
    avg_nps: float = Field(ge=0, le=10)

    @field_validator("avg_csat")
    @classmethod
    def validate_avg_csat(cls, v, values):
        """avg_csat computed from csat_scores"""
        all_reviews = values.get("positive_reviews", []) + values.get("negative_reviews", [])
        if not all_reviews:
            return v
        
        csat_scores = [r.csat_score for r in all_reviews]
        expected_avg = mean(csat_scores)
        
        if abs(v - expected_avg) > 0.01:
            raise ValueError(
                f"avg_csat {v:.2f} doesn't match computed {expected_avg:.2f}"
            )
        return v
    
    @field_validator("avg_nps")
    @classmethod
    def validate_avg_nps(cls, v, values):
        """avg_nps computed from nps_scores"""
        all_reviews = values.get("positive_reviews", []) + values.get("negative_reviews", [])
        if not all_reviews:
            return v
        
        nps_scores = [r.nps_score for r in all_reviews]
        expected_avg = mean(nps_scores)
        
        if abs(v - expected_avg) > 0.01:
            raise ValueError(
                f"avg_nps {v:.1f} doesn't match computed {expected_avg:.1f}"
            )
        return v


