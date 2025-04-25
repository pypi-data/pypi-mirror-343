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
        
        Examples:
        | AI Fallback Locator | Input Text | USERNAME_FIELD | myusername |
        | AI Fallback Locator | Input Text | css=#username | myusername | ai_description=the username input field |
        
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
            
            # For backward compatibility with existing test structures:
            # When called from a custom fallback pattern, we should not fail the test
            # but let the caller decide what to do with the failure
            if str(e).startswith("No AI description found"):
                logger.warn("Allowing test to continue despite missing AI description. This behavior is deprecated.")
                builtin = BuiltIn()
                try:
                    # Try to run the keyword with the primary locator as a last resort
                    primary_locator = self._get_primary_locator(builtin, locator_var)
                    if primary_locator:
                        return builtin.run_keyword(keyword_name, primary_locator, *args)
                except:
                    # If that fails too, raise the original exception
                    pass
            
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
        try:
            primary_locator = self._get_primary_locator(builtin, locator_var)
            
            # If locator is empty/None, try to use a default or infer from the context
            if not primary_locator:
                logger.warn(f"Empty primary locator provided. Trying to infer from context.")
                
                # For empty locators, create a generic context-based AI description
                if not ai_description:
                    # Use a generic description based on the keyword
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
            # Attempt with primary locator if it exists
            if primary_locator:
                logger.info(f"Attempting with primary locator: {primary_locator}")
                builtin.run_keyword(keyword_name, primary_locator, *args)
                logger.info(f"Successfully executed {keyword_name} with primary locator")
                return
        except Exception as e:
            logger.warn(f"Primary locator failed: {e}")
            
            # Get AI description (from parameter or derived from variable name)
            try:
                element_description = self._get_ai_description(builtin, locator_var, ai_description)
                
                # Try AI fallback with the description
                self._try_ai_fallback_with_description(builtin, keyword_name, primary_locator, element_description, args)
            except ValueError as desc_error:
                # If we couldn't get an AI description, try one more approach - look for any AI_ variable
                if "No AI description found" in str(desc_error):
                    fallback_desc = self._find_any_matching_ai_variable(builtin, keyword_name)
                    if fallback_desc:
                        logger.info(f"Using fallback AI description found in variables: {fallback_desc}")
                        self._try_ai_fallback_with_description(builtin, keyword_name, primary_locator, fallback_desc, args)
                    else:
                        raise
                else:
                    raise
    
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
                return primary_locator  # Can be None if variable exists but has no value
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
        
        # If we couldn't find a description, raise an error with helpful message
        if is_variable_name:
            error_msg = f"""No AI description found. You need to either:
1. Define the variable ${{{ai_var_name}}} with a description of the element, or
2. Provide the 'ai_description' parameter directly in your keyword call:
   AI Fallback Locator    Input Text    {locator_var}    value    ai_description=description of the element"""
        else:
            error_msg = f"""No AI description found. Since you're using a direct locator '{locator_var}', you must provide an AI description using the 'ai_description' parameter:
AI Fallback Locator    Input Text    {locator_var}    value    ai_description=description of the element"""
            
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
            
            # Get current page URL if possible for additional context
            page_url = None
            try:
                page_url = selenium_lib.get_location()
            except Exception:
                logger.debug("Could not get current page URL")
            
            # Generate AI locator
            try:
                # Try to use the AI API - pass the primary_locator as context
                ai_locator = self.ai_processor.generate_locator(
                    html, 
                    element_description, 
                    original_locator=primary_locator, 
                    page_url=page_url,
                    selenium_lib=selenium_lib
                )
            except Exception as api_error:
                # If API call fails, derive a simple CSS locator
                logger.warn(f"AI API error: {api_error}. Using a context-derived locator instead.")
                ai_locator = self.ai_processor.derive_contextual_locator(
                    html, 
                    element_description, 
                    original_locator=primary_locator
                )
                
            # Log some analytics data for monitoring
            logger.debug(f"Locator transformation: {primary_locator} → {ai_locator}")
            
            logger.info(f"AI generated locator: {ai_locator}")
            
            # *** SIMPLIFIED APPROACH: Just run the keyword directly ***
            # No enhanced interaction, no JavaScript fallbacks, just let Robot Framework handle it
            try:
                # First, try to wait for the element to be visible (but don't fail if it isn't)
                builtin.run_keyword_and_ignore_error("Wait Until Element Is Visible", ai_locator, "5s")
                
                # Then execute the requested keyword with the AI-generated locator
                builtin.run_keyword(keyword_name, ai_locator, *args)
                logger.info(f"Successfully executed {keyword_name} with AI-generated locator")
            except Exception as e:
                # If the keyword fails, let the exception propagate
                logger.error(f"Error executing {keyword_name} with AI-generated locator: {e}")
                raise
            
            # Store successful AI fallback
            if primary_locator:  # Only store if we had a primary locator
                self.locator_manager.store_locator_comparison(primary_locator, ai_locator)
            return
        except Exception as ai_error:
            error_msg = f"Both primary and AI fallback locators failed. Primary error: {primary_locator}. AI error: {ai_error}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def _find_any_matching_ai_variable(self, builtin, keyword_name):
        """
        Find any AI_ prefixed variable that might be relevant.
        This is a last resort mechanism for backward compatibility.
        
        :param builtin: BuiltIn instance
        :param keyword_name: The keyword name to help with context
        :return: An AI description if found, None otherwise
        """
        try:
            # Get all variables
            all_vars = builtin.get_variables()
            
            # Find AI_ variables
            ai_vars = {k: v for k, v in all_vars.items() if k.startswith('${AI_') and k.endswith('}') and v}
            
            if not ai_vars:
                return None
                
            # Try to find a match based on keyword context
            keyword_lower = keyword_name.lower()
            
            # Common action categories
            input_keywords = ["input", "text", "type", "enter", "fill"]
            interaction_keywords = ["click", "press", "select", "check", "choose", "toggle"]
            
            for var_name, description in ai_vars.items():
                var_name_lower = var_name.lower()
                
                # Match based on action type
                if any(k in keyword_lower for k in input_keywords):
                    if any(k in var_name_lower for k in ["input", "text", "field", "form", "enter"]):
                        logger.info(f"Found matching AI variable {var_name} for input action")
                        return description
                elif any(k in keyword_lower for k in interaction_keywords):
                    if any(k in var_name_lower for k in ["button", "link", "click", "select", "tab", "menu", "option"]):
                        logger.info(f"Found matching AI variable {var_name} for interaction action")
                        return description
            
            # If no specific match found but we have AI variables, use the first one as last resort
            first_description = next(iter(ai_vars.values()))
            logger.warn(f"No specific AI variable match found. Using first available as fallback: {first_description}")
            return first_description
            
        except Exception as e:
            logger.warn(f"Error looking for matching AI variables: {str(e)}")
            return None 