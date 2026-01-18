from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from statistics import mean

class Theme(BaseModel):
    """Granular theme extraction"""
    name: str = Field(description="Theme detected", max_length=50)
    sentiment: Literal["positive", "negative", "neutral"]
    strength: Literal["weak", "medium", "strong"]

class Emotion(BaseModel):
    """Detected emotions"""
    name: str = Field(description="Emotion detected")
    confidence: float = Field(ge=0, le=1)

class LLMExtractedContent(BaseModel):
    """Raw LLM response before validation"""
    sentiment_score: float = Field(ge=-1, le=1, description="-1 negative -> +1 positive")
    themes: List[Theme] = Field()
    emotions: List[Emotion] = Field()
    primary_praise: Optional[str] = Field(None, max_length=200)
    primary_complaint: Optional[str] = Field(None, max_length=200)
    extraction_confidence: float = Field(ge=0, le=1)

class RawReview(BaseModel):
    review_text: str = Field(min_length=10, max_length=10000)
    review_title: Optional[str] = Field(None, max_length=200)
    llm_content: LLMExtractedContent
    sentiment_category: Literal["positive", "neutral", "negative"]
    
    @field_validator("sentiment_category")
    @classmethod
    def validate_sentiment_category(cls, v, values):
        """Ensure sentiment_category matches llm_content.sentiment_score"""
        if "llm_content" not in values:
            raise ValueError("llm_content required for sentiment validation")
        
        score = values["llm_content"].sentiment_score
        expected = "positive" if score > 0.3 else "negative" if score < -0.3 else "neutral"
        
        if v != expected:
            raise ValueError(
                f"sentiment_category '{v}' doesn't match sentiment_score {score:.2f} "
                f"(expected '{expected}')"
            )
        return v

class RawReviewList(BaseModel):
    """Complete validated review aggregation with computed KPIs"""
    
    positive_reviews: List[RawReview] = Field(
        description="4-5 star reviews (sentiment_score > 0.3)"
    )
    negative_reviews: List[RawReview] = Field(
        description="1-3 star reviews (sentiment_score < -0.3)"
    )
    
    total_reviews_count: int = Field(gt=4, le=100)
    positive_reviews_count: int = Field(ge=0)
    negative_reviews_count: int = Field(ge=0)
    sentiment_score: float = Field(ge=-1, le=1)
    
    critical_issues: int = Field(ge=0)
    data_quality: float = Field(ge=0, le=1)
    
    computed_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator("total_reviews_count")
    @classmethod
    def validate_total_count(cls, v, values):
        """total_reviews_count == len(positive) + len(negative)"""
        pos_count = len(values.get("positive_reviews", []))
        neg_count = len(values.get("negative_reviews", []))
        expected = pos_count + neg_count
        
        if v != expected:
            raise ValueError(
                f"total_reviews_count {v} doesn't match actual {expected} reviews"
            )
        return v
    
    @field_validator("positive_reviews_count")
    @classmethod
    def validate_positive_count(cls, v, values):
        """positive_reviews_count == len(positive_reviews)"""
        actual = len(values.get("positive_reviews", []))
        if v != actual:
            raise ValueError(f"positive_reviews_count {v} != actual {actual}")
        return v
    
    @field_validator("negative_reviews_count")
    @classmethod
    def validate_negative_count(cls, v, values):
        """negative_reviews_count == len(negative_reviews)"""
        actual = len(values.get("negative_reviews", []))
        if v != actual:
            raise ValueError(f"negative_reviews_count {v} != actual {actual}")
        return v
    
    @field_validator("sentiment_score")
    @classmethod
    def validate_sentiment_score(cls, v, values):
        """sentiment_score = weighted average"""
        all_reviews = values.get("positive_reviews", []) + values.get("negative_reviews", [])
        if not all_reviews:
            return v
        
        scores = [r.llm_content.sentiment_score for r in all_reviews]
        expected_avg = mean(scores)
        
        if abs(v - expected_avg) > 0.01:
            raise ValueError(
                f"sentiment_score {v:.2f} doesn't match computed {expected_avg:.2f}"
            )
        return v
    
    @field_validator("critical_issues")
    @classmethod
    def validate_critical_issues(cls, v, values):
        """Count reviews needing immediate action"""
        all_reviews = values.get("positive_reviews", []) + values.get("negative_reviews", [])
        critical = sum(
            1 for r in all_reviews 
            if r.llm_content.extraction_confidence < 0.7 or 
               r.theme.strength == "strong" and r.theme.sentiment == "negative"
        )
        
        if v != critical:
            raise ValueError(f"critical_issues {v} != computed {critical}")
        return v
    
    @field_validator("data_quality")
    @classmethod
    def validate_data_quality(cls, v, values):
        """Quality score 0-1 based on confidence + completeness"""
        all_reviews = values.get("positive_reviews", []) + values.get("negative_reviews", [])
        if not all_reviews:
            return 0.0
        
        confidences = [r.llm_content.extraction_confidence for r in all_reviews]
        avg_confidence = mean(confidences)
        
        completeness = 1.0 if len(all_reviews) >= 5 else len(all_reviews) / 5
        expected_quality = (avg_confidence * 0.7) + (completeness * 0.3)
        
        if abs(v - expected_quality) > 0.05:
            raise ValueError(
                f"data_quality {v:.2f} doesn't match computed {expected_quality:.2f}"
            )
        return v

    class Config:
        validate_assignment = True
        extra = "forbid"

