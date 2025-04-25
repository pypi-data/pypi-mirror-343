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
                
                # For empty locators, use a generic context-based AI description
                if not ai_description:
                    # Try to infer a description based on the keyword
                    if "username" in keyword_name.lower() or "user" in keyword_name.lower():
                        ai_description = "the username input field"
                    elif "password" in keyword_name.lower():
                        ai_description = "the password input field"
                    elif "login" in keyword_name.lower() or "button" in keyword_name.lower() or "submit" in keyword_name.lower():
                        ai_description = "the login or submit button"
                    else:
                        # Use a very generic description as last resort
                        ai_description = f"the main interactive element for {keyword_name}"
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
            
            # Retry with AI-generated locator, but with enhanced interaction handling
            self._enhanced_interaction(builtin, keyword_name, ai_locator, args)
            
            # Store successful AI fallback
            if primary_locator:  # Only store if we had a primary locator
                self.locator_manager.store_locator_comparison(primary_locator, ai_locator)
            return
        except Exception as ai_error:
            error_msg = f"Both primary and AI fallback locators failed. Primary error: {primary_locator}. AI error: {ai_error}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def _enhanced_interaction(self, builtin, keyword_name, locator, args, max_retries=3, wait_time=1):
        """
        Enhanced interaction handling with automatic retries and wait conditions.
        
        :param builtin: BuiltIn instance
        :param keyword_name: The keyword to execute
        :param locator: The locator to use
        :param args: Additional arguments for the keyword
        :param max_retries: Maximum number of retries
        :param wait_time: Time to wait between retries
        """
        selenium_lib = builtin.get_library_instance('SeleniumLibrary')
        last_error = None
        
        # Special handling for different keyword types
        input_keywords = ["input text", "type text", "type into", "input password"]
        click_keywords = ["click", "click button", "click element", "click link"]
        
        # Normalize keyword name for comparison
        keyword_lower = keyword_name.lower()
        
        for attempt in range(max_retries):
            try:
                # Try various approaches based on keyword type
                if any(k in keyword_lower for k in input_keywords):
                    # For input keywords, try with extra steps
                    self._try_input_with_js_fallback(builtin, selenium_lib, keyword_name, locator, args)
                elif any(k in keyword_lower for k in click_keywords):
                    # For click keywords, try with extra steps
                    self._try_click_with_js_fallback(builtin, selenium_lib, keyword_name, locator, args)
                else:
                    # For other keywords, just try with a wait
                    builtin.run_keyword("Sleep", wait_time)
                    builtin.run_keyword(keyword_name, locator, *args)
                
                logger.info(f"Successfully executed {keyword_name} with enhanced interaction (attempt {attempt+1})")
                return True
            except Exception as e:
                last_error = e
                logger.warn(f"Attempt {attempt+1} failed: {str(e)}. Retrying...")
                builtin.run_keyword("Sleep", wait_time)
        
        # If we got here, all attempts failed
        raise last_error
    
    def _try_input_with_js_fallback(self, builtin, selenium_lib, keyword_name, locator, args):
        """
        Try input with JavaScript fallback if standard input fails.
        
        :param builtin: BuiltIn instance
        :param selenium_lib: SeleniumLibrary instance
        :param keyword_name: The keyword to execute
        :param locator: The locator to use
        :param args: Additional arguments for the keyword
        """
        # Try standard approach first
        try:
            # First try to scroll into view
            builtin.run_keyword_and_ignore_error("Execute JavaScript", f"arguments[0].scrollIntoView(true);", locator)
            
            # Wait for element to be visible
            builtin.run_keyword_and_ignore_error("Wait Until Element Is Visible", locator, "5s")
            
            # Try to use the keyword directly
            builtin.run_keyword(keyword_name, locator, *args)
            return
        except Exception as e:
            logger.warn(f"Standard input failed: {str(e)}. Trying with JavaScript...")
        
        # If we're here, standard approach failed. Try JavaScript approach.
        # Extract the text from args (assuming it's the first argument)
        text = args[0] if args else ""
        
        try:
            # Safer JavaScript approach without using private fields
            # Use standard properties and methods instead
            js_script = """
                try {
                    var element = arguments[0];
                    element.value = arguments[1];
                    
                    // Create and dispatch events for wider compatibility
                    var inputEvent = new Event('input', { bubbles: true });
                    element.dispatchEvent(inputEvent);
                    
                    var changeEvent = new Event('change', { bubbles: true });
                    element.dispatchEvent(changeEvent);
                    
                    return true;
                } catch(err) {
                    return "Error: " + err.message;
                }
            """
            
            result = builtin.run_keyword("Execute JavaScript", js_script, locator, text)
            
            if isinstance(result, str) and result.startswith("Error:"):
                raise Exception(f"JavaScript input failed: {result}")
            
            logger.info(f"Successfully set text via JavaScript")
        except Exception as js_error:
            logger.warn(f"JavaScript input approach failed: {str(js_error)}. Trying simpler approach...")
            
            # Try an even simpler approach as last resort
            builtin.run_keyword("Execute JavaScript", 
                               "arguments[0].value = arguments[1];", 
                               locator, text)
            logger.info(f"Set text using simplified JavaScript approach")
    
    def _try_click_with_js_fallback(self, builtin, selenium_lib, keyword_name, locator, args):
        """
        Try click with JavaScript fallback if standard click fails.
        
        :param builtin: BuiltIn instance
        :param selenium_lib: SeleniumLibrary instance
        :param keyword_name: The keyword to execute
        :param locator: The locator to use
        :param args: Additional arguments for the keyword
        """
        # Try standard approach first
        try:
            # First try to scroll into view
            builtin.run_keyword_and_ignore_error("Execute JavaScript", f"arguments[0].scrollIntoView(true);", locator)
            
            # Wait for element to be visible
            builtin.run_keyword_and_ignore_error("Wait Until Element Is Visible", locator, "5s")
            
            # Wait for element to be enabled
            builtin.run_keyword_and_ignore_error("Wait Until Element Is Enabled", locator, "5s")
            
            # Try to use the keyword directly
            builtin.run_keyword(keyword_name, locator, *args)
            return
        except Exception as e:
            logger.warn(f"Standard click failed: {str(e)}. Trying with JavaScript...")
        
        try:
            # If we're here, standard approach failed. Try JavaScript approach.
            # Use safer JavaScript without private fields
            js_script = """
                try {
                    var element = arguments[0];
                    
                    // First try the standard click
                    element.click();
                    return true;
                } catch(err1) {
                    try {
                        // If standard click fails, try creating and dispatching a click event
                        var clickEvent = new MouseEvent('click', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        });
                        element.dispatchEvent(clickEvent);
                        return true;
                    } catch(err2) {
                        return "Error: " + (err1.message + " AND " + err2.message);
                    }
                }
            """
            
            result = builtin.run_keyword("Execute JavaScript", js_script, locator)
            
            if isinstance(result, str) and result.startswith("Error:"):
                raise Exception(f"JavaScript click failed: {result}")
                
            logger.info(f"Successfully clicked via JavaScript")
        except Exception as js_error:
            logger.warn(f"JavaScript click approach failed: {str(js_error)}. Trying simpler approach...")
            
            # Try an even simpler approach as last resort
            builtin.run_keyword("Execute JavaScript", 
                               "arguments[0].click();", 
                               locator)
            logger.info(f"Clicked using simplified JavaScript approach")
    
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
            for var_name, description in ai_vars.items():
                var_name_lower = var_name.lower()
                
                # Match based on action type
                if 'input' in keyword_lower or 'text' in keyword_lower:
                    if 'input' in var_name_lower or 'text' in var_name_lower or 'field' in var_name_lower or 'username' in var_name_lower or 'password' in var_name_lower:
                        logger.info(f"Found matching AI variable {var_name} for input action")
                        return description
                        
                elif 'click' in keyword_lower or 'button' in keyword_lower or 'submit' in keyword_lower:
                    if 'button' in var_name_lower or 'submit' in var_name_lower or 'click' in var_name_lower:
                        logger.info(f"Found matching AI variable {var_name} for click action")
                        return description
                
                # If no specific matches, look for username or password in variable name
                elif 'username' in var_name_lower:
                    return description
                elif 'password' in var_name_lower:
                    return description
                elif 'button' in var_name_lower or 'submit' in var_name_lower:
                    return description
            
            # If no specific match found but we have AI variables, use the first one as last resort
            first_description = next(iter(ai_vars.values()))
            logger.warn(f"No specific AI variable match found. Using first available as fallback: {first_description}")
            return first_description
            
        except Exception as e:
            logger.warn(f"Error looking for matching AI variables: {str(e)}")
            return None 