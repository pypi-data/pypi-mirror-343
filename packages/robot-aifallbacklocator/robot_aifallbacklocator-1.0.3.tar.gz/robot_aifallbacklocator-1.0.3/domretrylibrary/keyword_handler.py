#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import traceback
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

class KeywordHandler:
    
    def __init__(self, ai_processor, locator_manager):
        self.ai_processor = ai_processor
        self.locator_manager = locator_manager
        self.browser_lib = None
        self.context = None
        self.original_var_name = None
    
    def ai_fallback_locator(self, keyword_name, locator_var, *args, ai_description=None):
        try:
            return self._ai_fallback_locator_impl(keyword_name, locator_var, *args, ai_description=ai_description)
        except Exception as e:
            logger.error(f"Error in AI Fallback Locator: {str(e)}")
            logger.debug(traceback.format_exc())
            
            if str(e).startswith("No AI description found"):
                logger.warn("Allowing test to continue despite missing AI description. This behavior is deprecated.")
                builtin = BuiltIn()
                try:
                    primary_locator = self._get_primary_locator(builtin, locator_var)
                    if primary_locator:
                        return builtin.run_keyword(keyword_name, primary_locator, *args)
                except:
                    pass
            
            raise
    
    def _get_ai_description(self, ai_description, primary_locator=None):
        if ai_description:
            logger.info(f"Using provided AI description: '{ai_description}'")
            return ai_description
            
        from robot.libraries.BuiltIn import BuiltIn
        builtin = BuiltIn()
        
        all_vars = builtin.get_variables()
        
        if hasattr(self, 'original_var_name') and self.original_var_name:
            ai_var_name = "${AI_" + self.original_var_name + "}"
            if ai_var_name in all_vars:
                ai_description = all_vars[ai_var_name]
                logger.info(f"Found AI description from original variable {self.original_var_name}: '{ai_description}'")
                self.original_var_name = None
                return ai_description
        
        if not primary_locator.startswith(('id=', 'xpath=', 'css=', 'name=', 'class=', 'tag=', 'link=', 'partial link=')):
            ai_var_name = "${AI_" + primary_locator + "}"
            if ai_var_name in all_vars:
                ai_description = all_vars[ai_var_name]
                logger.info(f"Found AI description in variable {ai_var_name}: '{ai_description}'")
                return ai_description
        else:
            locator_type, locator_value = primary_locator.split('=', 1)
            
            originating_var = None
            for var_name, var_value in all_vars.items():
                if var_name.startswith('${') and var_name.endswith('}') and var_value == primary_locator:
                    originating_var = var_name
                    logger.debug(f"Found originating variable {originating_var} for locator {primary_locator}")
                    
                    ai_var_name = "${AI_" + var_name[2:-1] + "}"
                    if ai_var_name in all_vars:
                        ai_description = all_vars[ai_var_name]
                        logger.info(f"Found AI description in variable {ai_var_name}: '{ai_description}'")
                        return ai_description
            
            if not originating_var:
                ai_var_name = f"${{AI_{locator_type}={locator_value}}}"
                if ai_var_name in all_vars:
                    ai_description = all_vars[ai_var_name]
                    logger.info(f"Found AI description in variable {ai_var_name}: '{ai_description}'")
                    return ai_description
                
                for var_name, var_value in all_vars.items():
                    if var_name.startswith('${AI_') and isinstance(var_value, str):
                        base_name = var_name[5:-1]
                        
                        base_var = "${" + base_name + "}"
                        if base_var in all_vars and all_vars[base_var] == primary_locator:
                            logger.info(f"Found AI description by reconstructing variables: {var_name}: '{var_value}'")
                            return var_value
        
        error_msg = f"No AI description found for {primary_locator}. Please provide an AI description using the 'ai_description' parameter."
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def _ai_fallback_locator_impl(self, keyword_name, locator_var, *args, ai_description=None):
        builtin = BuiltIn()
        
        try:
            primary_locator = self._get_primary_locator(builtin, locator_var)
            
            if not primary_locator:
                logger.warn(f"Empty primary locator provided. Trying to infer from context.")
                
                if not ai_description:
                    keyword_lower = keyword_name.lower()
                    if "input" in keyword_lower or "text" in keyword_lower or "type" in keyword_lower:
                        ai_description = f"the input field for {keyword_name}"
                    elif "click" in keyword_lower or "press" in keyword_lower or "select" in keyword_lower:
                        ai_description = f"the interactive element for {keyword_name}"
                    else:
                        ai_description = f"the main element targeted by {keyword_name}"
        except Exception as e:
            logger.warn(f"Error getting primary locator: {str(e)}. Proceeding with fallback mechanism.")
            primary_locator = locator_var
        
        try:
            if primary_locator:
                logger.info(f"Attempting with primary locator: {primary_locator}")
                builtin.run_keyword(keyword_name, primary_locator, *args)
                logger.info(f"Successfully executed {keyword_name} with primary locator")
                return
        except Exception as e:
            logger.warn(f"Primary locator failed: {e}")
            
            try:
                element_description = self._get_ai_description(ai_description, primary_locator)
                logger.info(f"Got AI description for {locator_var}: '{element_description}'")
                
                self._try_ai_fallback_with_description(builtin, keyword_name, primary_locator, element_description, args)
            except ValueError as desc_error:
                if "No AI description found" in str(desc_error):
                    fallback_desc = self._find_any_matching_ai_variable(builtin, keyword_name=keyword_name)
                    if fallback_desc:
                        logger.info(f"Using fallback AI description found in variables: {fallback_desc}")
                        self._try_ai_fallback_with_description(builtin, keyword_name, primary_locator, fallback_desc, args)
                    else:
                        raise
                else:
                    raise
    
    def _get_primary_locator(self, builtin, locator_var):
        if isinstance(locator_var, str) and locator_var.startswith(('id=', 'xpath=', 'css=', 'name=', 'class=', 'tag=', 'link=', 'partial link=')):
            logger.info(f"Using directly provided locator: {locator_var}")
            all_vars = builtin.get_variables()
            for var_name, var_value in all_vars.items():
                if var_name.startswith('${') and var_name.endswith('}') and var_value == locator_var:
                    logger.info(f"Found that locator {locator_var} comes from variable {var_name}")
                    self.original_var_name = var_name[2:-1]
                    break
            return locator_var
        
        is_variable_name = isinstance(locator_var, str) and not locator_var.startswith('/') and not locator_var.startswith('//') and not locator_var.startswith('xpath=')
        
        if is_variable_name:
            try:
                primary_locator = builtin.get_variable_value("${" + locator_var + "}")
                return primary_locator
            except Exception as e:
                logger.error(f"Error getting variable value: {str(e)}")
                raise
        else:
            return locator_var
    
    def _try_ai_fallback_with_description(self, builtin, keyword_name, primary_locator, element_description, args):
        try:
            selenium_lib = builtin.get_library_instance('SeleniumLibrary')
            html = selenium_lib.get_source()
            
            page_url = None
            try:
                page_url = selenium_lib.get_location()
            except Exception:
                logger.debug("Could not get current page URL")
            
            try:
                ai_locator = self.ai_processor.generate_locator(
                    html, 
                    element_description, 
                    original_locator=primary_locator, 
                    page_url=page_url,
                    selenium_lib=selenium_lib
                )
            except Exception as api_error:
                logger.warn(f"AI API error: {api_error}. Using a context-derived locator instead.")
                raise api_error
                
            logger.debug(f"Locator transformation: {primary_locator} → {ai_locator}")
            logger.info(f"AI generated locator: {ai_locator}")
            
            try:
                builtin.run_keyword("Wait Until Element Is Visible", ai_locator, "5s")
                builtin.run_keyword(keyword_name, ai_locator, *args)
                logger.info(f"Successfully executed {keyword_name} with AI-generated locator")
            except Exception as e:
                logger.error(f"Error executing {keyword_name} with AI-generated locator: {e}")
                raise
            
            if primary_locator:
                self.locator_manager.store_locator_comparison(primary_locator, ai_locator)
            return
        except Exception as e:
            logger.error(f"AI fallback failed: {str(e)}")
            raise
    
    def _find_any_matching_ai_variable(self, builtin, keyword_name=None):
        try:
            variables = builtin.get_variables()
            
            ai_vars = {}
            for var_name, var_value in variables.items():
                if var_name.startswith('${AI_') and isinstance(var_value, str):
                    ai_vars[var_name] = var_value
            
            if not ai_vars:
                return None
                
            if keyword_name:
                keyword_lower = keyword_name.lower()
                
                for var_name, var_value in ai_vars.items():
                    if keyword_lower in var_name.lower() or keyword_lower in var_value.lower():
                        return var_value
            
            if ai_vars:
                return list(ai_vars.values())[0]
                
            return None
        except Exception:
            return None 