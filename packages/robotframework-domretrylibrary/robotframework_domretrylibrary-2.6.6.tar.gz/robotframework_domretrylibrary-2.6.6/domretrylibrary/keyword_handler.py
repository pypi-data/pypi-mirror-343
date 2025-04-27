#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

class KeywordHandler:
    
    def __init__(self, ai_processor, locator_manager):
        self.ai_processor = ai_processor
        self.locator_manager = locator_manager
    
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
                element_description = self._get_ai_description(builtin, locator_var, ai_description)
                
                self._try_ai_fallback_with_description(builtin, keyword_name, primary_locator, element_description, args)
            except ValueError as desc_error:
                if "No AI description found" in str(desc_error):
                    fallback_desc = self._find_any_matching_ai_variable(builtin, keyword_name="Input Text")
                    if fallback_desc:
                        logger.info(f"Using fallback AI description found in variables: {fallback_desc}")
                        self._try_ai_fallback_with_description(builtin, keyword_name, primary_locator, fallback_desc, args)
                    else:
                        raise
                else:
                    raise
    
    def _get_primary_locator(self, builtin, locator_var):
        is_variable_name = isinstance(locator_var, str) and not locator_var.startswith('css=') and not locator_var.startswith('xpath=')
        
        if is_variable_name:
            try:
                primary_locator = builtin.get_variable_value("${" + locator_var + "}")
                return primary_locator
            except Exception as e:
                logger.error(f"Error getting variable value: {str(e)}")
                raise
        else:
            return locator_var
    
    def _get_ai_description(self, builtin, locator_var, ai_description=None):
        if ai_description:
            logger.info(f"Using provided AI description: {ai_description}")
            return ai_description
        
        is_direct_locator = isinstance(locator_var, str) and (locator_var.startswith('css=') or locator_var.startswith('xpath='))
        is_variable_name = isinstance(locator_var, str) and not is_direct_locator
        
        try:
            all_vars = builtin.get_variables()
            
            if is_direct_locator:
                matching_vars = []
                for var_name, var_value in all_vars.items():
                    if var_value == locator_var and var_name.startswith('${') and var_name.endswith('}'):
                        base_var_name = var_name[2:-1]
                        matching_vars.append(base_var_name)
                
                for base_var_name in matching_vars:
                    ai_var_name = f"AI_{base_var_name}"
                    try:
                        ai_description = builtin.get_variable_value("${" + ai_var_name + "}")
                        if ai_description:
                            logger.info(f"Found AI description from {ai_var_name} for direct locator {locator_var}")
                            return ai_description
                    except Exception:
                        continue
        except Exception as e:
            logger.warn(f"Error searching for matching variables: {str(e)}")
            
        if is_variable_name:
            ai_var_name = f"AI_{locator_var}"
            try:
                ai_description = builtin.get_variable_value("${" + ai_var_name + "}")
                if ai_description:
                    logger.info(f"Found AI description from {ai_var_name}: {ai_description}")
                    return ai_description
            except Exception as var_error:
                logger.warn(f"Error getting AI description variable: {str(var_error)}")
        
        try:
            fallback_desc = self._find_any_matching_ai_variable(builtin, keyword_name="Input Text")
            if fallback_desc:
                logger.info(f"Using fallback AI description found in variables: {fallback_desc}")
                return fallback_desc
        except Exception as fallback_error:
            logger.warn(f"Error finding fallback AI variable: {str(fallback_error)}")
        
        if is_direct_locator:
            error_msg = f"""No AI description found. Since you're using a direct locator '{locator_var}', you must provide an AI description using the 'ai_description' parameter:
AI Fallback Locator    Input Text    {locator_var}    value    ai_description=description of the element"""
        else:
            error_msg = f"""No AI description found. You need to either:
1. Define the variable ${{{ai_var_name if is_variable_name else 'AI_VARIABLE_NAME'}}} with a description of the element, or
2. Provide the 'ai_description' parameter directly in your keyword call:
   AI Fallback Locator    Input Text    {locator_var}    value    ai_description=description of the element"""
            
        logger.error(error_msg)
        raise ValueError(error_msg)
    
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
                ai_locator = self.ai_processor.derive_contextual_locator(
                    html, 
                    element_description, 
                    original_locator=primary_locator
                )
                
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
        except Exception as ai_error:
            error_msg = f"Both primary and AI fallback locators failed. Primary error: {primary_locator}. AI error: {ai_error}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def _find_any_matching_ai_variable(self, builtin, keyword_name):
        try:
            all_vars = builtin.get_variables()
            
            ai_vars = {k: v for k, v in all_vars.items() if k.startswith('${AI_') and k.endswith('}') and v}
            
            if not ai_vars:
                return None
            
            keyword_lower = keyword_name.lower()
            
            input_keywords = ["input", "text", "type", "enter", "fill", "write", "insert", "put"]
            interaction_keywords = ["click", "press", "select", "check", "choose", "toggle", "tap", "activate", "open"]
            wait_keywords = ["wait", "until", "for", "visible", "present", "enabled", "displayed"]
            get_keywords = ["get", "fetch", "read", "extract", "retrieve"]
            
            scored_vars = []
            
            for var_name, description in ai_vars.items():
                var_name_lower = var_name.lower()
                score = 0
                
                if any(k in keyword_lower for k in input_keywords):
                    if any(k in var_name_lower for k in ["input", "text", "field", "form", "enter", "username", "email", "password"]):
                        score += 10
                elif any(k in keyword_lower for k in interaction_keywords):
                    if any(k in var_name_lower for k in ["button", "link", "click", "select", "tab", "menu", "option", "checkbox", "radio"]):
                        score += 10
                elif any(k in keyword_lower for k in wait_keywords):
                    if any(k in var_name_lower for k in ["load", "appear", "display", "show", "visible"]):
                        score += 10
                elif any(k in keyword_lower for k in get_keywords):
                    if any(k in var_name_lower for k in ["value", "text", "content", "data"]):
                        score += 10
                
                keyword_words = set(keyword_lower.replace('_', ' ').split())
                var_words = set(var_name_lower.replace('_', ' ').replace('${ai', '').replace('}', '').split())
                
                exact_matches = keyword_words.intersection(var_words)
                score += len(exact_matches) * 5
                
                scored_vars.append((var_name, description, score))
            
            scored_vars.sort(key=lambda x: x[2], reverse=True)
            
            if scored_vars:
                highest_score_var = scored_vars[0]
                if highest_score_var[2] > 0:
                    logger.info(f"Selected AI variable {highest_score_var[0]} with relevance score {highest_score_var[2]}")
                    return highest_score_var[1]
            
            first_description = next(iter(ai_vars.values()))
            logger.warn(f"No specific AI variable match found. Using first available as fallback: {first_description}")
            return first_description
            
        except Exception as e:
            logger.warn(f"Error looking for matching AI variables: {str(e)}")
            return None 