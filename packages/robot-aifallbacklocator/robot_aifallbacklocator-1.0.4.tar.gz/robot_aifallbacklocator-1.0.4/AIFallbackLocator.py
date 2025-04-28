from domretrylibrary.core import DomRetryLibrary
from dotenv import load_dotenv
import os

class AIFallbackLocator(DomRetryLibrary):
    def __init__(self, api_key=None, openai_api_url=None, model=None, locator_storage_file="locator_comparison.json", transformation_cache_file=None):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key, URL, and model from environment variables with fallbacks
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        openai_api_url = openai_api_url or os.getenv('OPENAI_API_URL')
        model = model or os.getenv('OPENAI_MODEL')
        
        # Call the parent class constructor with the parameters
        super().__init__(
            openai_api_url=openai_api_url,
            api_key=api_key,
            model=model,
            locator_storage_file=locator_storage_file,
            transformation_cache_file=transformation_cache_file
        )

__version__ = "1.0.4" 