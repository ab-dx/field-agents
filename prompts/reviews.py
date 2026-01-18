review_template = """
**TASK**: Collect maximum customer reviews for "%s" on %s

**REQUIREMENTS**:
1. **MAXIMIZE COVERAGE**: Fetch 5-100 reviews (prioritize most recent)
2. **DIVERSITY**: Mix of ratings (1-5 stars), different dates/authors
3. **RECENCY**: Focus on last 30-90 days when possible
4. **RELEVANCE**: Only reviews mentioning company/product
5. **MINIMUM ALTERATION**: Return review content as is, or with negligible modifications if required.
"""

def fetch_reviews_chrome(target, source):
    return review_template % (target, f"chrome via {source} website")

def fetch_reviews_app(target, source):
    return review_template % (target, f"{source} app")

if __name__ == "__main__":
    print(fetch_reviews_chrome("a","b"))
