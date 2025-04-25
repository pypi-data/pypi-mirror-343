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
        self.variable_mappings = {}
    
    def ai_fallback_locator(self, keyword_name, locator_var, *args):
        """
        Add AI fallback to any locator-based keyword.
        
        This keyword will first try to use the primary locator, and if it fails,
        it will use the AI-generated locator as a fallback.
        
        Example:
        | AI Fallback Locator | Input Text | USERNAME_FIELD | myusername |
        
        :param keyword_name: The keyword to execute (e.g., Input Text, Click Element)
        :param locator_var: Variable name or value (with or without ${})
        :param args: Additional arguments for the keyword
        """
        try:
            return self._ai_fallback_locator_impl(keyword_name, locator_var, *args)
        except Exception as e:
            logger.error(f"Error in AI Fallback Locator: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    
    def _ai_fallback_locator_impl(self, keyword_name, locator_var, *args):
        """
        Implementation of the AI fallback locator keyword.
        
        :param keyword_name: The keyword to execute
        :param locator_var: Variable name or value
        :param args: Additional arguments for the keyword
        """
        builtin = BuiltIn()
        
        # Extract primary locator and variable name
        primary_locator, var_name = self._extract_locator_and_name(builtin, locator_var, args)
        
        try:
            # Attempt with primary locator
            logger.info(f"Attempting with primary locator: {primary_locator}")
            builtin.run_keyword(keyword_name, primary_locator, *args)
            logger.info(f"Successfully executed {keyword_name} with primary locator")
            return
        except Exception as e:
            logger.warn(f"Primary locator failed: {e}")
            
            # Use AI fallback
            self._try_ai_fallback(builtin, keyword_name, primary_locator, var_name, args)
    
    def _extract_locator_and_name(self, builtin, locator_var, args):
        """
        Extract the primary locator and variable name from the input.
        
        :param builtin: BuiltIn instance
        :param locator_var: Variable name or value
        :param args: Additional arguments
        :return: Tuple of (primary_locator, var_name)
        """
        # Determine if we have a variable name or variable value
        is_variable_name = isinstance(locator_var, str) and not locator_var.startswith('css=') and not locator_var.startswith('xpath=')
        
        if is_variable_name:
            # We have a variable name, get its value
            try:
                primary_locator = builtin.get_variable_value("${" + locator_var + "}")
                if primary_locator is None:
                    raise ValueError(f"Variable '${{{locator_var}}}' not found or is None")
                var_name = locator_var
            except Exception as e:
                logger.error(f"Error getting variable value: {str(e)}")
                raise
        else:
            # We already have a variable value, find the corresponding variable name
            primary_locator = locator_var
            
            # Update the variable mappings to allow reverse lookups
            try:
                all_variables = builtin.get_variables()
                for name, value in all_variables.items():
                    if name.startswith('${') and name.endswith('}') and value == primary_locator and not name.startswith('${AI_'):
                        self.variable_mappings[value] = name[2:-1]  # Store without ${} wrapping
            except Exception as e:
                logger.warn(f"Error mapping variables: {str(e)}")
            
            # Try to find the variable name for this value
            var_name = self.variable_mappings.get(primary_locator)
            
            if not var_name:
                # As a fallback, use a default if specified (like "USERNAME_FIELD")
                if len(args) > 1 and isinstance(args[-1], str) and args[-1] == "USERNAME_FIELD":
                    var_name = "USERNAME_FIELD"
                    logger.warn(f"Using default variable name '{var_name}' as actual variable name couldn't be determined")
                else:
                    logger.warn(f"Could not determine variable name for: {primary_locator}. Using 'USERNAME_FIELD' as default.")
                    var_name = "USERNAME_FIELD"
        
        return primary_locator, var_name
    
    def _try_ai_fallback(self, builtin, keyword_name, primary_locator, var_name, args):
        """
        Try AI fallback when primary locator fails.
        
        :param builtin: BuiltIn instance
        :param keyword_name: The keyword to execute
        :param primary_locator: Primary locator that failed
        :param var_name: Variable name
        :param args: Additional arguments for the keyword
        """
        # Use AI_ prefixed version of the same variable
        ai_var_name = f"AI_{var_name}"
        try:
            ai_description = builtin.get_variable_value("${" + ai_var_name + "}")
        except Exception as var_error:
            logger.error(f"Error getting AI description variable: {str(var_error)}")
            raise Exception(f"Failed to get AI description from ${{{ai_var_name}}}: {str(var_error)}")
        
        if not ai_description:
            error_msg = f"Primary locator failed and no AI description found for {ai_var_name}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        logger.info(f"Found AI description from {ai_var_name}: {ai_description}")
        
        try:
            # Get HTML content
            selenium_lib = builtin.get_library_instance('SeleniumLibrary')
            html = selenium_lib.get_source()
            
            # Generate AI locator
            try:
                # Try to use the AI API
                ai_locator = self.ai_processor.generate_locator(html, ai_description)
            except Exception as api_error:
                # If API call fails, derive a simple CSS locator
                logger.warn(f"AI API error: {api_error}. Using a context-derived locator instead.")
                ai_locator = self.ai_processor.derive_contextual_locator(html, ai_description)
            
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