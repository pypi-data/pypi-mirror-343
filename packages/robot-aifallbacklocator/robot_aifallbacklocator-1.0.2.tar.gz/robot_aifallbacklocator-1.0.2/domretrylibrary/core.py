#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import traceback
from robot.api import logger
from robot.api.deco import keyword
from dotenv import load_dotenv
import json
import time
import re

from .ai_processor import AIProcessor
from .locator_manager import LocatorManager
from .keyword_handler import KeywordHandler

VERSION = "1.0.2"

class DomRetryLibrary:

    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LIBRARY_VERSION = VERSION
    ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'

    def __init__(self, openai_api_url="https://api.openai.com/v1/chat/completions", api_key=None, model="gpt-4o", locator_storage_file="locator_comparison.json", transformation_cache_file=None):
        try:
            load_dotenv()
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                logger.warn("No OpenAI API key provided. AI fallback will not work properly!")
            else:
                masked_key = self.api_key[:7] + "..." + self.api_key[-4:] if len(self.api_key) > 11 else "***masked***"
                logger.info(f"Using OpenAI API with format: {masked_key}")
            self.ai_processor = AIProcessor(api_key=self.api_key, api_url=openai_api_url, model=model, transformation_cache_file=transformation_cache_file)
            self.locator_manager = LocatorManager(locator_storage_file=locator_storage_file)
            self.keyword_handler = KeywordHandler(self.ai_processor, self.locator_manager)
        except Exception as e:
            logger.error(f"Error initializing DomRetryLibrary: {str(e)}")
            logger.debug(traceback.format_exc())
            raise

    @keyword(name="AI Fallback Locator")
    def ai_fallback_locator(self, keyword_name, locator_var, *args, ai_description=None):
        try:
            return self.keyword_handler.ai_fallback_locator(keyword_name, locator_var, *args, ai_description=ai_description)
        except Exception as e:
            logger.error(f"Error in AI Fallback Locator: {str(e)}")
            raise

    @keyword
    def clear_locator_history(self):
        self.locator_manager.clear_history()
    
    @keyword
    def clear_transformation_cache(self):
        self.ai_processor.transformation_cache = {}
        self.ai_processor._save_transformation_cache()
        logger.info("Transformation cache has been cleared")



