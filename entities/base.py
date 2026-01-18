from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from pydantic import ValidationInfo

class Theme(BaseModel):
    name: str = Field(max_length=50, description="Theme detected")
    sentiment: Literal["positive", "negative", "neutral"]
    strength: Literal["weak", "medium", "strong"]

class Emotion(BaseModel):
    name: str = Field(description="Emotion detected")
    confidence: float = Field(ge=0, le=1)

class LLMExtractedContent(BaseModel):
    sentiment_score: float = Field(ge=-1, le=1)
    themes: List[Theme]
    emotions: List[Emotion]
    primary_praise: Optional[str] = Field(None)
    primary_complaint: Optional[str] = Field(None)
    extraction_confidence: float = Field(ge=0, le=1)

class RawReview(BaseModel):
    review_text: str = Field(min_length=1, max_length=10000)
    review_title: Optional[str] = Field(None, max_length=200)
    llm_content: LLMExtractedContent
    sentiment_category: Literal["positive", "neutral", "negative"]

