"""
Query classification agent
Categorizes customer queries into Technical, Billing, or General
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


def categorize_inquiry(state: CustomerSupportState) -> Dict[str, str]:
    """
    Categorize customer query into: Technical, Billing, or General
    
    Args:
        state: Current workflow state containing customer_query
        
    Returns:
        Dictionary with query_category field
    """
    query = state["customer_query"]
    logger.info(f"Categorizing query: {query[:100]}...")
    
    # Category classification prompt
    CATEGORY_PROMPT = """
    You are an intelligent query classifier for a tutoring support system.
    Your goal is to accurately categorize the following teacher or tutor query into one of three distinct categories.

    ---

    **Categories**

    1. 🧮 **Academic & Curriculum Analytics**
    Queries about **curriculum structure, subject topics, academic content by year group,**
    or analytical insights about student data and performance.

    Includes:
    - Understanding what topics or subjects are taught in a particular year or curriculum stage.
    - Curriculum alignment or coverage questions.
    - Analyzing, comparing, or reporting on academic performance, attendance patterns, or exam results.

    Examples:
    - "What topics are covered in Year 8 Maths?"
    - "Compare the average math performance between Year 5 and Year 6."
    - "Show me attendance patterns for Year 9 students."

    2. 💳 **Billing, Payments & Administrative**
    Queries related to pricing, invoices, refunds, subscriptions, payment failures, 
    account upgrades/downgrades, or other financial or account issues.

    3. 🧾 **General / Teaching Assistance**
    Queries that ask for help **creating or preparing teaching materials** — such as 
    lesson plans, quizzes, worksheets, or study guides.
    Also includes platform or account questions not related to curriculum or analytics.

    ---

    **Instructions**

    - Assign the query to exactly **one** category.
    - Output **only** the category name, exactly as written:
    `Academic & Curriculum Analytics`, `Billing, Payments & Administrative`, or `General / Teaching Assistance`
    - Do **not** explain or justify your choice.
    - If a query fits more than one category, select the **primary intent** of the query.

    ---

    **Examples**

    | Query | Category |
    |--------|-----------|
    | "Show me my students’ attendance trend for Year 8" | Academic & Curriculum Analytics |
    | "Generate a lesson on fractions and a short quiz to practice" | General / Teaching Assistance |
    | "Prepare a Year 9 science test based on the UK curriculum" | General / Teaching Assistance |
    | "Compare the average math performance between Year 5 and Year 6" | Academic & Curriculum Analytics |
    | "How do I download my last month’s invoice?" | Billing, Payments & Administrative |
    | "Where can I reset my tutor account password?" | Billing, Payments & Administrative |
    | "What topic do you teach in maths for Year 8?" | Academic & Curriculum Analytics |

    ---

    Customer Query:
    {customer_query}

    Category:
    """
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            openai_api_key=settings.openai_api_key
        )
        
        # Create prompt and invoke
        prompt = ChatPromptTemplate.from_template(CATEGORY_PROMPT)
        chain = prompt | llm
        
        response = chain.invoke({"customer_query": query})
        category = response.content.strip()
        
        # Validate category
        valid_categories = ["Academic & Curriculum Analytics", "Billing, Payments & Administrative", "General / Teaching Assistance"]
        if category not in valid_categories:
            logger.warning(f"Invalid category '{category}', defaulting to 'General / Teaching Assistance'")
            category = "General / Teaching Assistance"

        logger.info(f"Query categorized as: {category}")
        #remove this test code
        #print("Category Yogi:", category)
        
        return {"query_category": category}
        
    except Exception as e:
        logger.error(f"Error categorizing query: {e}")
        # Default to General on error
        return {"query_category": "General / Teaching Assistance"}

# %%
if __name__ == "__main__":
    demo_state = CustomerSupportState(customer_query="what topic you teach in maths for year 8?")
    result = categorize_inquiry(demo_state)
    print(result)
# %%
