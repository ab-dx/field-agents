from pydantic import BaseModel, Field, computed_field
from typing import List, Union, Optional
from statistics import mean
from datetime import datetime


from entities.app_review import (GlassdoorEmployeeReview, GlassdoorEmployeeBenifit, GlassdoorEmployeeSalary)

AnyEmployeeReview = Union[GlassdoorEmployeeReview, GlassdoorEmployeeBenifit, GlassdoorEmployeeSalary]

class EmployeeReviewReport(BaseModel):
    comp_name: Optional[str] = None
    reviews: List[AnyEmployeeReview] = []
    
    # Precomputed by Glassdoor
    overall_star_rating: Optional[float] = Field(None, ge=1, le=5)  
    recommend_to_friend_pct: Optional[float] = Field(None, ge=0, le=100)  
    ceo_approval_pct: Optional[float] = Field(None, ge=0, le=100)  
    no_of_reviews: Optional[int] = Field(None, ge=0)  
    
    computed_at: datetime = Field(default_factory=datetime.now)
    
    
    
    # Computing for each review, salary & benifits
    @computed_field
    def sentiment_score(self) -> float:
        return mean(r.llm_content.sentiment_score for r in self.reviews)
        
        
    @computed_field
    def avg_esat(self) -> float:
        if not self.reviews:
            return 0.0
        return round(mean(r.esat_score for r in self.reviews), 2)
        
    @computed_field
    def avg_enps_rating(self) -> float:
        """Average of individual enps_scores (-100 to 100)"""
        if not self.reviews:
            return 0.0
        return round(mean(r.enps_score for r in self.reviews), 2)
        
    @computed_field
    def true_enps_score(self) -> float:
        """INDUSTRY STANDARD enps: %Promoters(9-10) - %Detractors(0-6)"""
        if not self.reviews:
            return 0.0
        scores = [r.recommend_score for r in self.reviews]
        total = len(scores)
        
        
        promoters = sum(1 for x in scores if x >=9)
        detracters = sum(1 for x in scores if x <=6)
        return round((promoters/total) - (detracters/total) * 100, 2)
        
    @computed_field
    def avg_review_star(self) -> float:
        """ONLY GlassdoorEmployeeReview star_rating"""
        if not self.reviews:
            return 0.0
        review_stars = [
            r.star_rating for r in self.reviews
            if isinstance(r, GlassdoorEmployeeReview) and r.star_rating
        ]
        return round(mean(review_stars), 2)
    
    @computed_field
    def avg_benifit_star(self) -> float:
        """ONLY GlassdoorEmployeeBenifit star_rating"""
        if not self.reviews:
            return 0.0
        benifit_stars = [
            r.star_rating for r in self.reviews
            if isinstance(r, GlassdoorEmployeeBenifit) and r.star_rating
        ]
        return round(mean(benifit_stars), 2)
        
    @computed_field
    def avg_salary_star(self) -> float:
        """ONLY GlassdoorEmployeeSalary star_rating"""
        if not self.reviews:
            return 0.0
        salary_stars = [
            r.star_rating for r in self.reviews
            if isinstance(r, GlassdoorEmployeeSalary) and r.star_rating
        ]
        return round(mean(salary_stars), 2) 

    @computed_field
    def avg_glassdoor_star(self) -> float:
        """Combines ALL star_ratings (Reviews + Salaries + Benefits)"""
        if not self.reviews:
            return 0.0
        star_ratings = [
            r.star_rating for r in self.reviews
            if hasattr(r, "star_rating") and r.star_rating is not None
        ]
        return round(mean(star_ratings), 2)
    
    @computed_field
    def data_quality(self) -> float:
        avg_conf = mean(r.llm_content.extraction_confidence for r in self.reviews)
        completeness = min(len(self.reviews) / 5, 1.0)
        return (avg_conf * 0.7) + (completeness * 0.3)