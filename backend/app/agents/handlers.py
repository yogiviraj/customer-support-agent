"""
Response generation handlers using RAG
Generates contextual responses based on knowledge base retrieval
"""
import logging
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.models.schemas import CustomerSupportState
from app.config.settings import get_settings
from app.database.vectordb import search_knowledge_base

logger = logging.getLogger(__name__)
settings = get_settings()


def generate_technical_response(state: CustomerSupportState) -> Dict[str, str]:
    """
    Generate academic support response using RAG
    
    Args:
        state: Current workflow state
        
    Returns:
        Dictionary with final_response
    """
    query = state["customer_query"]
    category = state["query_category"]
    
    logger.info(f"Generating academic response for: {query[:100]}...")
    
    try:
        # Retrieve relevant documents with academic filter
        relevant_docs = search_knowledge_base(
            query=query,
            category_filter="General / Teaching Assistance" if category.lower() == "general / teaching assistance" else None
        )
        
        # Extract content from retrieved documents
        retrieved_content = "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in relevant_docs
        ])
        
        if not retrieved_content:
            retrieved_content = "No specific documentation found for this query."
        
        # Academic response prompt
        ACADEMIC_PROMPT = """
        You are an academic support specialist with deep expertise in UK curricula and student analytics.

        Craft a clear and detailed academic support response for the following customer query.
        Use the retrieved knowledge base information below to provide accurate, curriculum-aligned guidance.

        Guidelines:
        - Be precise about subjects, year groups, and learning goals
        - Include concrete examples, learning strategies, or assessment tips when relevant
        - Reference curriculum sources when applicable
        - If the retrieved information is incomplete, acknowledge it and suggest next steps or resources
        - Keep the response professional, supportive, and teacher-friendly

        Retrieved Knowledge Base Information:
        {retrieved_content}

        Customer Query:
        {customer_query}

        Academic Support Response:
        """
        
        # Initialize LLM
        llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            openai_api_key=settings.openai_api_key
        )
        
        # Generate response
        prompt = ChatPromptTemplate.from_template(ACADEMIC_PROMPT)
        chain = prompt | llm
        
        response = chain.invoke({
            "customer_query": query,
            "retrieved_content": retrieved_content
        })
        
        final_response = response.content.strip()
        logger.info("Academic response generated successfully")
        
        return {"final_response": final_response}
        
    except Exception as e:
        logger.error(f"Error generating academic response: {e}")
        return {
            "final_response": "I apologize, but I encountered an error while processing your academic question. "
                             "Please contact our academic support team at support@company.com for immediate assistance."
        }


def generate_billing_response(state: CustomerSupportState) -> Dict[str, str]:
    """
    Generate billing support response using RAG
    
    Args:
        state: Current workflow state
        
    Returns:
        Dictionary with final_response
    """
    query = state["customer_query"]
    category = state["query_category"]
    
    logger.info(f"Generating billing response for: {query[:100]}...")
    
    try:
        # Retrieve relevant documents with billing filter
        relevant_docs = search_knowledge_base(
            query=query,
            category_filter="Billing, Payments & Administrative" if category.lower() == "billing, payments & administrative" else None
        )
        
        # Extract content from retrieved documents
        retrieved_content = "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in relevant_docs
        ])
        
        if not retrieved_content:
            retrieved_content = "No specific billing information found for this query."
        
        # Billing response prompt
        BILLING_PROMPT = """
        You are a billing support specialist focused on helping customers with financial matters.
        
        Craft a clear and detailed billing support response for the following customer query.
        Use the retrieved knowledge base information below to provide accurate answers about pricing,
        payments, invoices, refunds, or subscription matters.
        
        Guidelines:
        - Be clear about pricing, payment terms, and policies
        - Include specific details like pricing tiers, payment methods, and timeframes
        - If discussing refunds or disputes, be empathetic and helpful
        - Reference official policies when applicable
        - For account-specific issues, direct the customer to the appropriate channel
        - Keep the response professional and reassuring
        
        Retrieved Knowledge Base Information:
        {retrieved_content}
        
        Customer Query:
        {customer_query}
        
        Billing Support Response:
        """
        
        # Initialize LLM
        llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            openai_api_key=settings.openai_api_key
        )
        
        # Generate response
        prompt = ChatPromptTemplate.from_template(BILLING_PROMPT)
        chain = prompt | llm
        
        response = chain.invoke({
            "customer_query": query,
            "retrieved_content": retrieved_content
        })
        
        final_response = response.content.strip()
        logger.info("Billing response generated successfully")
        
        return {"final_response": final_response}
        
    except Exception as e:
        logger.error(f"Error generating billing response: {e}")
        return {
            "final_response": "I apologize, but I encountered an error while processing your billing question. "
                             "Please contact our billing team at billing@company.com for immediate assistance."
        }


def generate_general_response(state: CustomerSupportState) -> Dict[str, str]:
    """
    Generate general support response using RAG
    
    Args:
        state: Current workflow state
        
    Returns:
        Dictionary with final_response
    """
    query = state["customer_query"]
    category = state["query_category"]
    
    logger.info(f"Generating general response for: {query[:100]}...")
    
    try:
        # Retrieve relevant documents with general filter
        relevant_docs = search_knowledge_base(
            query=query,
            category_filter="General / Teaching Assistance" if category.lower() == "general / teaching assistance" else None
        )
        
        # Extract content from retrieved documents
        retrieved_content = "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in relevant_docs
        ])
        
        if not retrieved_content:
            retrieved_content = "No specific information found for this query."
        
        # General response prompt
        GENERAL_PROMPT = """
        You are a customer support representative helping customers with general inquiries.
        
        Craft a clear and helpful response for the following customer query.
        Use the retrieved knowledge base information below to provide accurate information about
        our company, policies, support channels, or general questions.
        
        Guidelines:
        - Be friendly, professional, and helpful
        - Provide complete and accurate information
        - Include relevant links or contact information when appropriate
        - If the question is outside your knowledge, direct them to the right resource
        - Keep the response concise but thorough
        
        Retrieved Knowledge Base Information:
        {retrieved_content}
        
        Customer Query:
        {customer_query}
        
        Support Response:
        """
        
        # Initialize LLM
        llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            openai_api_key=settings.openai_api_key
        )
        
        # Generate response
        prompt = ChatPromptTemplate.from_template(GENERAL_PROMPT)
        chain = prompt | llm
        
        response = chain.invoke({
            "customer_query": query,
            "retrieved_content": retrieved_content
        })
        
        final_response = response.content.strip()
        logger.info("General response generated successfully")
        
        return {"final_response": final_response}
        
    except Exception as e:
        logger.error(f"Error generating general response: {e}")
        return {
            "final_response": "I apologize, but I encountered an error while processing your question. "
                             "Please contact our support team at support@company.com for assistance."
        }
