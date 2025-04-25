#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

class KeywordHandler:
    """
    Implements Robot Framework keywords for DOM locator retries.
    """
    
    def __init__(self, ai_processor, locator_manager):
        """
        Initialize the keyword handler.
        
        :param ai_processor: Instance of AIProcessor
        :param locator_manager: Instance of LocatorManager
        """
        self.ai_processor = ai_processor
        self.locator_manager = locator_manager
    
    def ai_fallback_locator(self, keyword_name, locator_var, *args, ai_description=None):
        """
        Add AI fallback to any locator-based keyword.
        
        This keyword will first try to use the primary locator, and if it fails,
        it will use the AI-generated locator as a fallback.
        
        Example:
        | AI Fallback Locator | Input Text | USERNAME_FIELD | myusername |
        | AI Fallback Locator | Input Text | USERNAME_FIELD | myusername | ai_description=Input field with label Username |
        
        :param keyword_name: The keyword to execute (e.g., Input Text, Click Element)
        :param locator_var: Variable name or value (with or without ${})
        :param args: Additional arguments for the keyword
        :param ai_description: Optional direct AI description (overrides AI_ variable lookup)
        """
        try:
            return self._ai_fallback_locator_impl(keyword_name, locator_var, *args, ai_description=ai_description)
        except Exception as e:
            logger.error(f"Error in AI Fallback Locator: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    
    def _ai_fallback_locator_impl(self, keyword_name, locator_var, *args, ai_description=None):
        """
        Implementation of the AI fallback locator keyword.
        
        :param keyword_name: The keyword to execute
        :param locator_var: Variable name or value
        :param args: Additional arguments for the keyword
        :param ai_description: Optional direct AI description
        """
        builtin = BuiltIn()
        
        # Get the primary locator
        primary_locator = self._get_primary_locator(builtin, locator_var)
        
        try:
            # Attempt with primary locator
            logger.info(f"Attempting with primary locator: {primary_locator}")
            builtin.run_keyword(keyword_name, primary_locator, *args)
            logger.info(f"Successfully executed {keyword_name} with primary locator")
            return
        except Exception as e:
            logger.warn(f"Primary locator failed: {e}")
            
            # Get AI description (from parameter or derived from variable name)
            element_description = self._get_ai_description(builtin, locator_var, ai_description)
            
            # Try AI fallback with the description
            self._try_ai_fallback_with_description(builtin, keyword_name, primary_locator, element_description, args)
    
    def _get_primary_locator(self, builtin, locator_var):
        """
        Get the primary locator value.
        
        :param builtin: BuiltIn instance
        :param locator_var: Variable name or value
        :return: The locator value
        """
        # Check if it's a variable name (not starting with css= or xpath=)
        is_variable_name = isinstance(locator_var, str) and not locator_var.startswith('css=') and not locator_var.startswith('xpath=')
        
        if is_variable_name:
            # It's a variable name, get its value
            try:
                primary_locator = builtin.get_variable_value("${" + locator_var + "}")
                if primary_locator is None:
                    raise ValueError(f"Variable '${{{locator_var}}}' not found or is None")
                return primary_locator
            except Exception as e:
                logger.error(f"Error getting variable value: {str(e)}")
                raise
        else:
            # It's already a locator value
            return locator_var
    
    def _get_ai_description(self, builtin, locator_var, ai_description=None):
        """
        Get the AI description, either from the parameter or by deriving from the variable name.
        
        :param builtin: BuiltIn instance
        :param locator_var: Variable name or value
        :param ai_description: Optional direct AI description
        :return: The AI description to use
        """
        # If description is provided directly, use it (highest priority)
        if ai_description:
            logger.info(f"Using provided AI description: {ai_description}")
            return ai_description
            
        # Otherwise, try to get it from AI_VARIABLE_NAME pattern
        is_variable_name = isinstance(locator_var, str) and not locator_var.startswith('css=') and not locator_var.startswith('xpath=')
        
        if is_variable_name:
            # Get AI description from AI_VARNAME
            ai_var_name = f"AI_{locator_var}"
            try:
                ai_description = builtin.get_variable_value("${" + ai_var_name + "}")
                if ai_description:
                    logger.info(f"Found AI description from {ai_var_name}: {ai_description}")
                    return ai_description
            except Exception as var_error:
                logger.warn(f"Error getting AI description variable: {str(var_error)}")
        
        # If we couldn't find a description, raise an error
        error_msg = f"No AI description found. Either provide 'ai_description' parameter or define ${{{ai_var_name if is_variable_name else 'AI_*'}}}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    def _try_ai_fallback_with_description(self, builtin, keyword_name, primary_locator, element_description, args):
        """
        Try AI fallback using the provided element description.
        
        :param builtin: BuiltIn instance
        :param keyword_name: The keyword to execute
        :param primary_locator: Primary locator that failed
        :param element_description: Description of the element for AI
        :param args: Additional arguments for the keyword
        """
        try:
            # Get HTML content
            selenium_lib = builtin.get_library_instance('SeleniumLibrary')
            html = selenium_lib.get_source()
            
            # Generate AI locator
            try:
                # Try to use the AI API
                ai_locator = self.ai_processor.generate_locator(html, element_description)
            except Exception as api_error:
                # If API call fails, derive a simple CSS locator
                logger.warn(f"AI API error: {api_error}. Using a context-derived locator instead.")
                ai_locator = self.ai_processor.derive_contextual_locator(html, element_description)
            
            logger.info(f"AI generated locator: {ai_locator}")
            
            # Retry with AI-generated locator
            builtin.run_keyword(keyword_name, ai_locator, *args)
            logger.info(f"Successfully executed {keyword_name} with AI locator")
            
            # Store successful AI fallback
            self.locator_manager.store_locator_comparison(primary_locator, ai_locator)
            return
        except Exception as ai_error:
            error_msg = f"Both primary and AI fallback locators failed. Primary error: {primary_locator}. AI error: {ai_error}"
            logger.error(error_msg)
            raise Exception(error_msg) 