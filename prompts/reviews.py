review_template = """
TASK: Collect maximum customer reviews for "{app}" on {platform}

**REQUIREMENTS**:
1. **MAXIMIZE COVERAGE**: Fetch 5-100 reviews (prioritize most recent)
2. **DIVERSITY**: Mix of ratings (1-5 stars), different dates/authors
3. **RECENCY**: Focus on last 30-90 days when possible
4. **RELEVANCE**: Only reviews mentioning company/product
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
- Capture star rating for each review if visible
- calculate sentiment using the given function, and nps from csat/star_rating using the given function for each review 
"""

def fetch_reviews_app(app: str, platform: str) -> str:
    platform = platform.lower().strip()
    if platform == "reddit":
        return fetch_reviews_reddit(app)
    if platform == "playstore":
        return fetch_reviews_playstore(app)
    if platform == "x":
        return fetch_reviews_x(app)
    raise ValueError("platform must be: reddit | playstore | x")


if __name__ == "__main__":
    print(fetch_reviews_playstore("Neural DSP"))
