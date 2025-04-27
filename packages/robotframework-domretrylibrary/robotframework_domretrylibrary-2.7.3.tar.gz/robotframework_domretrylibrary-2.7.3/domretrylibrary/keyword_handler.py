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
        
        # Get all variables to search for matches
        all_vars = builtin.get_variables()
        
        # For direct locators (e.g., xpath=foo), try to find matching AI variables
        if primary_locator and primary_locator.startswith(('id=', 'xpath=', 'css=', 'name=', 'class=', 'tag=', 'link=', 'partial link=')):
            locator_type, locator_value = primary_locator.split('=', 1)
            
            # First try exact matches for AI_{locator_type}={value} pattern
            ai_var_name = f"${{AI_{locator_type}={locator_value}}}"
            if ai_var_name in all_vars:
                ai_description = all_vars[ai_var_name]
                logger.info(f"Found AI description in variable {ai_var_name}: '{ai_description}'")
                return ai_description
                
            # Then try for variable references containing this locator
            for var_name, var_value in all_vars.items():
                if isinstance(var_value, str) and var_value == primary_locator and var_name.startswith('${') and var_name.endswith('}'):
                    base_var_name = var_name[2:-1]  # Remove ${ and }
                    ai_var_name = "${AI_" + base_var_name + "}"
                    if ai_var_name in all_vars:
                        ai_description = all_vars[ai_var_name]
                        logger.info(f"Found AI description in variable {ai_var_name}: '{ai_description}'")
                        return ai_description
            
            # Try a fuzzy match based on the locator value
            for var_name, var_value in all_vars.items():
                if var_name.startswith('${AI_') and isinstance(var_value, str):
                    if locator_value.lower() in var_name.lower():
                        logger.info(f"Found fuzzy matching AI description in variable {var_name}: '{var_value}'")
                        return var_value
                        
        # If no AI description was found, raise an error
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
                raise api_error  # Just raise the error directly rather than trying a fallback
                
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
    
    def _extract_field_name(self, variable_name):
        """Try to extract a meaningful name from the variable name."""
        if not variable_name or not isinstance(variable_name, str):
            return None
            
        # If it's a direct locator, extract the relevant part
        if '=' in variable_name:
            parts = variable_name.split('=', 1)
            variable_name = parts[1]
            
        # Remove common prefixes/suffixes
        clean_name = variable_name
        for prefix in ['BTN_', 'FLD_', 'TXT_', 'LNK_', 'CHECKBOX_', 'RADIO_', 'SELECT_', 'DROPDOWN_', 'css=', 'xpath=', '//', '/']:
            if clean_name.startswith(prefix):
                clean_name = clean_name[len(prefix):]
                
        for suffix in ['_BUTTON', '_FIELD', '_INPUT', '_LINK', '_CHECKBOX', '_RADIO', '_SELECT', '_DROPDOWN', '_ELEMENT']:
            if clean_name.endswith(suffix):
                clean_name = clean_name[:-len(suffix)]
                
        return clean_name
    
    def _find_any_matching_ai_variable(self, builtin, keyword_name=None):
        """Find any AI_ variable that might be related to the element we're looking for."""
        try:
            # Get all variables
            variables = builtin.get_variables()
            
            # Find any AI_ variables
            ai_vars = {}
            for var_name, var_value in variables.items():
                if var_name.startswith('${AI_') and isinstance(var_value, str):
                    ai_vars[var_name] = var_value
            
            if not ai_vars:
                return None
                
            # If we have a keyword name, try to use that for matching
            if keyword_name:
                keyword_lower = keyword_name.lower()
                
                for var_name, var_value in ai_vars.items():
                    if keyword_lower in var_name.lower() or keyword_lower in var_value.lower():
                        return var_value
            
            # If no match found based on keyword, return the first AI_ variable (as last resort)
            if ai_vars:
                return list(ai_vars.values())[0]
                
            return None
        except Exception:
            return None 