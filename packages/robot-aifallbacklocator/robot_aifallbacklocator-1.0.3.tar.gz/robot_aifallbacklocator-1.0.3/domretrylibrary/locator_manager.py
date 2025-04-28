#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from robot.api import logger

class LocatorManager:
    
    def __init__(self, locator_storage_file="locator_comparison.json"):
        self.locator_storage_file = locator_storage_file
        self.locator_comparison = []
        
        self._load_comparisons()
    
    def _load_comparisons(self):
        if os.path.exists(self.locator_storage_file):
            try:
                with open(self.locator_storage_file, 'r') as f:
                    self.locator_comparison = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error loading {self.locator_storage_file}. Starting with empty comparison list.")
            except Exception as e:
                logger.error(f"Unexpected error loading locator storage file: {str(e)}")
    
    def store_locator_comparison(self, primary_locator, ai_locator):
        try:
            entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "primary_locator": primary_locator,
                "ai_locator": ai_locator
            }
            
            self.locator_comparison.append(entry)
            
            with open(self.locator_storage_file, 'w') as f:
                json.dump(self.locator_comparison, f, indent=2)
            
            logger.console(f"\nLocator Comparison: {entry}")
            logger.console(f"Primary Locator (Failed): {primary_locator}")
            logger.console(f"AI Locator (Succeeded): {ai_locator}\n")
        except Exception as e:
            logger.warn(f"Failed to store locator comparison: {str(e)}")
    
    def get_historical_locators(self, primary_locator=None):
        if primary_locator:
            return [comp for comp in self.locator_comparison if comp.get("primary_locator") == primary_locator]
        return self.locator_comparison
    
    def clear_history(self):
        self.locator_comparison = []
        if os.path.exists(self.locator_storage_file):
            try:
                os.remove(self.locator_storage_file)
                logger.info(f"Removed locator storage file: {self.locator_storage_file}")
            except Exception as e:
                logger.error(f"Failed to remove storage file: {str(e)}")
                with open(self.locator_storage_file, 'w') as f:
                    json.dump([], f) 