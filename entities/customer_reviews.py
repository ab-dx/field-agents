from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from datetime import datetime

class Theme(BaseModel):
    """Granular theme extraction"""
    name: str = Field(description="Theme detected",max_length=50)
    sentiment: Literal["positive", "negative", "neutral"]
    strength: Literal["weak", "medium", "strong"]

class Emotion(BaseModel):
    """Detected emotions"""
    name: str = Field(description="Emotion detected")
    confidence: float = Field(ge=0, le=1)

class LLMExtractedContent(BaseModel):
    """Raw LLM response before validation"""
    csat_score: int = Field(ge=1, le=5)  # Customer satisfaction 1-5
    nps_score: int = Field(ge=0, le=10)  # Net Promoter Score 0-10
    sentiment_score: float = Field(ge=-1, le=1)  # -1 negative → +1 positive
    themes: List[Theme]
    emotions: List[Emotion]
    primary_praise: Optional[str] = None
    primary_complaint: Optional[str] = None
    extraction_confidence: float = Field(ge=0, le=1)  # LLM self-confidence

class RawReview(BaseModel):
    review_text: str = Field(min_length=1, max_length=10000)
    review_title: Optional[str] = None
    star_rating: float = Field(ge=1, le=5)
    theme: Theme
    emotion: Emotion
    llm_content: LLMExtractedContent
    sentiment_category: Literal["positive", "neutral", "negative"] = Field(
        description="Computed from sentiment_score: >0.3=positive, <-0.3=negative"
    )
    @validator("sentiment_category")
    def compute_sentiment_category(cls, v, values):
        score = values["llm_content"].sentiment_score
        if score > 0.3:
            return "positive"
        elif score < -0.3:
            return "negative"
        return "neutral"

class RawReviewList(BaseModel):
    positive_reviews: List[RawReview] = Field(description="positive reviews")
    negative_reviews: List[RawReview] = Field(description="negative reviews")
    total_reviews_count: int
    positive_reviews_count: int
    negative_reviews_count: int
    avg_csat: float  # 1-5
    avg_nps: float   # 0-10
    sentiment_score: float  # -1 to +1
    critical_issues: int
    actionable_reviews: int
    data_quality: float  # 0-1
    computed_at: datetime = Field(default_factory=datetime.now)
