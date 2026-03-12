from langchain_groq import ChatGroq
from app.config.config import GROQ_API_KEY

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(groq_api_key: str = GROQ_API_KEY):
    try:
        logger.info("Loading LLM from Groq")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        llm = ChatGroq(
            groq_api_key = groq_api_key,
            model_name = "llama-3.3-70b-versatile",
            temperature = 0.3,
            max_tokens = 1024
        )
        logger.info("Groq LLM loaded successfully...")
        return llm
    except Exception as e:
        error_message = CustomException("Failed to load Groq LLM", e)
        logger.error(str(error_message))
        return None