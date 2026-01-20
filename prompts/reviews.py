review_template = """
TASK: Collect maximum customer reviews for "{app}" on {platform}

**REQUIREMENTS**:
1. **MAXIMIZE COVERAGE**: Fetch 5-100 reviews (prioritize most recent)
2. **DIVERSITY**: Mix of ratings (1-5 stars), different dates/authors
3. **RECENCY**: Focus on last 30-90 days when possible
4. **RELEVANCE**: Strictly Only reviews mentioning company/product and talking about the pros/cons
5. **MINIMUM ALTERATION**: Return review content as is, or with negligible modifications if required.
"""

def fetch_reviews_reddit(app: str) -> str:
    return review_template.format(app=app, platform="Reddit app") + """
- Capture upvotes if visible
- calculate sentiment, csat, and nps for each review using the given function
"""

def fetch_reviews_x(app: str) -> str:
    return review_template.format(app=app, platform="X (Twitter) app") + """
- Prefer recent posts
- Capture likes/reposts/replies if visible
- calculate sentiment, csat, and nps for each review using the given function
"""

def fetch_reviews_playstore(app: str) -> str:
    return review_template.format(app=app, platform="Google Play Store app") + """
- Also collect app-level stats:
  1) total number of reviews
  2) number of downloads/installs (the range shown)
  3) overall app rating
- Capture star rating for each review if visible, set that as csat
- calculate sentiment using the given function, and nps from csat/star_rating using the given function for each review 
"""


def fetch_reviews_glassdoor(company: str) -> str:
    return review_template.format(app=company, platform="Glassdoor company") + """
- Also collect company-level stats from Glassdoor overview:
  1) overall_star_rating (1-5★)
  2) no_of_reviews (total review count)  
  3) recommend_to_friend_pct (% recommend)
  4) ceo_approval_pct (% CEO approval)
  
- Navigate tabs and capture for each item:
  1) Reviews tab → GlassdoorEmployeeReview (star_rating, pros, cons, likes)
  2) Salaries tab → GlassdoorEmployeeSalary (base_salary, star_rating, jobs) 
  3) Benefits tab → GlassdoorEmployeeBenifit (benifit, star_rating, likes)
  
- For each review/salary/benefit:
  - Capture star_rating if visible
  - Calculate sentiment using vader_sentiment_tool() on text fields (pros, cons, post)
  - Convert sentiment → employee_satisfaction using sentiment_to_employee_satisfaction()
  - Convert sentiment → recommend_score using sentiment_to_eNPS_rating()
  - Set eNPS_score from recommend_to_friend_pct conversion: ((pct/100)*200)-100
"""



def fetch_reviews_app(app: str, platform: str) -> str:
    platform = platform.lower().strip()
    if platform == "reddit":
        return fetch_reviews_reddit(app)
    if platform == "playstore":
        return fetch_reviews_playstore(app)
    if platform == "x":
        return fetch_reviews_x(app)
    if platform == "glassdoor":
        return fetch_reviews_glassdoor(company = app)
    raise ValueError("platform must be: reddit | playstore | x | glassdoor")


if __name__ == "__main__":
    print(fetch_reviews_playstore("Neural DSP"))
