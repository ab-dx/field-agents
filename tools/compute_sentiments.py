from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def vader_sentiment_tool(text: str, **kwargs) -> float:
    return analyzer.polarity_scores(text)["compound"]

def sentiment_to_csat_tool(sentiment_score: float, **kwargs) -> int:
    csat = round(((sentiment_score + 1) / 2) * 4 + 1)
    return max(1, min(5, int(csat)))

def sentiment_to_nps_rating_tool(sentiment_score: float, **kwargs) -> int:
    nps = round(((sentiment_score + 1) / 2) * 10)
    return max(0, min(10, int(nps)))

def csat_to_nps_rating_tool(csat_score: int, **kwargs) -> int:
    c = max(1, min(5, int(round(csat_score))))
    return {1: 2, 2: 4, 3: 6, 4: 8, 5: 10}[c]

def sentiment_to_esat_tool(sentiment_score: float, **kwargs) -> int:
    esat = round(((sentiment_score + 1) / 2) * 4 + 1)
    return max(1, min(5, int(esat)))
    
def sentiment_to_enps_rating(sentiment_score:
 float, **kwargs) -> int:
    recommend = round(((sentiment_score + 1) / 2) * 10 + 1)
    return max(0, min(10, int(recommend)))
    
def esat_to_recommend(esat_score: int, **kwargs) -> int:
    e = max(1, min(5, int(round(esat_score))))
    return {1: 2, 2: 4, 3: 6, 4: 8, 5: 10}[e]

ALL_TOOLS = {
    "vader_sentiment": {
        "arguments": ["text"],
        "description": "Returns compound sentiment score in [-1, 1]",
        "function": vader_sentiment_tool,
    },
    
    
    # Customer tools
    "sentiment_to_csat": {
        "arguments": ["sentiment_score"],
        "description": "Convert sentiment [-1,1] into CSAT [1,5]",
        "function": sentiment_to_csat_tool,
    },
    "sentiment_to_nps_rating": {
        "arguments": ["sentiment_score"],
        "description": "Convert sentiment [-1,1] into NPS rating [0,10]",
        "function": sentiment_to_nps_rating_tool,
    },
    "csat_to_nps_rating": {
        "arguments": ["csat_score"],
        "description": "Convert CSAT [1,5] into NPS rating [0,10]",
        "function": csat_to_nps_rating_tool,
    },
    
    
    # Employee tools
    "sentiment_to_esat": {
        "arguments": ["sentiment_score"],
        "description": "Convert sentiment[-1, 1] into ESAT [1, 5]",
        "function": sentiment_to_esat_tool
    },
    "sentiment_to_enps_rating": {
        "arguments": ["sentiment_score"],
        "description": "Convert sentiment [-1,1] into eNPS rating [0,10]",
        "function": sentiment_to_enps_rating,
    },
    "esat_to_recommend_rating": {
        "arguments": ["esat_score"],
        "description": "Convert ESAT [1,5] into Recommend Score rating [0,10]",
        "function": esat_to_recommend,
    }
    
}

TOOLS_REDDIT_X = {
    "vader_sentiment": ALL_TOOLS["vader_sentiment"],
    "sentiment_to_csat": ALL_TOOLS["sentiment_to_csat"],
    "sentiment_to_nps_rating": ALL_TOOLS["sentiment_to_nps_rating"],
}

TOOLS_PLAYSTORE = {
    "vader_sentiment": ALL_TOOLS["vader_sentiment"],
    "csat_to_nps_rating": ALL_TOOLS["csat_to_nps_rating"],
}


TOOLS_GLASSDOOR = {
    "vader_sentiment": ALL_TOOLS["vader_sentiment"],
    "sentiment_to_esat": ALL_TOOLS["sentiment_to_esat"],
    "sentiment_to_enps_rating": ALL_TOOLS["sentiment_to_enps_rating"],
    "esat_to_recommend_rating": ALL_TOOLS["esat_to_recommend_rating"]
}