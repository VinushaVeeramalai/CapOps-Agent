from pydantic import BaseModel, Field

class SentimentResult(BaseModel):
    sentiment: str = Field(description="Must be one of: positive, neutral, frustrated, angry")
    score: int = Field(description="CX score between 0 and 100")
    recommended_action: str = Field(description="Recommended next action")
    priority: str = Field(description="P1, P2, or P3 based on sentiment")

def analyze_sentiment(text: str) -> dict:
    lowered = (text or "").lower()
    angry_terms = ["angry", "terrible", "worst", "unacceptable", "furious"]
    frustrated_terms = ["frustrated", "not working", "issue", "problem", "delay"]
    positive_terms = ["thanks", "great", "awesome", "helpful", "good"]

    if any(term in lowered for term in angry_terms):
        result = SentimentResult(sentiment="angry", score=20, recommended_action="Escalate to human support", priority="P1")
    elif any(term in lowered for term in frustrated_terms):
        result = SentimentResult(sentiment="frustrated", score=45, recommended_action="Provide direct troubleshooting steps", priority="P2")
    elif any(term in lowered for term in positive_terms):
        result = SentimentResult(sentiment="positive", score=90, recommended_action="Proceed with current flow", priority="P3")
    else:
        result = SentimentResult(sentiment="neutral", score=65, recommended_action="Continue conversation", priority="P3")

    return result.dict()
