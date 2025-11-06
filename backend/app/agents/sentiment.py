"""
Sentiment analysis agent
Analyzes customer query sentiment as Positive, Neutral, or Negative
"""
#%%
import logging
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.models.schemas import CustomerSupportState
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def analyze_sentiment(state: CustomerSupportState) -> Dict[str, str]:
    """
    Analyze sentiment of customer query
    
    Args:
        state: Current workflow state containing customer_query
        
    Returns:
        Dictionary with query_sentiment field
    """
    query = state["customer_query"]
    logger.info(f"Analyzing sentiment for query: {query[:100]}...")
    
    # Sentiment analysis prompt
    SENTIMENT_PROMPT = """
    You are a sentiment analysis expert. Your job is to analyze the emotional tone of customer queries
    to help prioritize support requests.

    Analyze the customer query below and classify its sentiment into ONE of these categories:

    1. **Positive**: Customer is happy, satisfied, expressing gratitude, or being complimentary.
       Examples: "Thank you for the great service!", "I love this feature!"

    2. **Neutral**: Customer is asking a straightforward question without strong emotion.
       Examples: "What payment methods do you support?", "How do I integrate with AWS?"

    3. **Negative**: Customer is frustrated, angry, disappointed, or expressing dissatisfaction.
       Examples: "This is terrible!", "I'm very frustrated", "This doesn't work at all"

    Return ONLY the sentiment category (Positive, Neutral, or Negative).
    Do not include any explanation, just the sentiment.

    Customer Query:
    {customer_query}

    Sentiment:
    """
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            openai_api_key=settings.openai_api_key
        )
        
        # Create prompt and invoke
        prompt = ChatPromptTemplate.from_template(SENTIMENT_PROMPT)
        chain = prompt | llm
        
        response = chain.invoke({"customer_query": query})
        sentiment = response.content.strip()
        
        # Validate sentiment
        valid_sentiments = ["Positive", "Neutral", "Negative"]
        if sentiment not in valid_sentiments:
            logger.warning(f"Invalid sentiment '{sentiment}', defaulting to 'Neutral'")
            sentiment = "Neutral"
        
        logger.info(f"Query sentiment analyzed as: {sentiment}")
        
        return {"query_sentiment": sentiment}
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        # Default to Neutral on error
        return {"query_sentiment": "Neutral"}

# %%
if __name__ == "__main__":
    # quick manual test
    from types import SimpleNamespace

    # 1) fake state shaped like CustomerSupportState
    # if your real state is a Pydantic model with .model_dump(), adjust accordingly
    test_state = {
        "customer_query": "I'm really unhappy, the lesson portal is not loading!"
    }

    result = analyze_sentiment(test_state)
    print("Sentiment result:", result)

    # try another one
    test_state2 = {
        "customer_query": "Thanks for helping me with the maths practice 😊"
    }
    result2 = analyze_sentiment(test_state2)
    print("Sentiment result:", result2)
# %%
