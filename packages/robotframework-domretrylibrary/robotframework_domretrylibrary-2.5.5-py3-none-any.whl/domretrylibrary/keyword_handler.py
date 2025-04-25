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
            
            # *** EDGE-COMPATIBLE APPROACH: Special handling for Microsoft Edge ***
            try:
                # Detect browser type
                browser_name = self._detect_browser_name(selenium_lib)
                logger.debug(f"Detected browser: {browser_name}")
                
                # First, try to wait for the element to be visible
                builtin.run_keyword_and_ignore_error("Wait Until Element Is Visible", ai_locator, "5s")
                
                # For Edge, use special handling
                if browser_name and "edge" in browser_name.lower():
                    logger.info("Microsoft Edge detected, using Edge-specific handling")
                    
                    # Different handling based on keyword type
                    keyword_lower = keyword_name.lower()
                    
                    if "input text" in keyword_lower or "type" in keyword_lower:
                        # For input text operations in Edge
                        self._enhanced_browser_input_text(builtin, selenium_lib, ai_locator, args, browser_name)
                        logger.info(f"Successfully used Edge-compatible input for {ai_locator}")
                    elif "click" in keyword_lower:
                        # For click operations in Edge
                        self._enhanced_browser_click(builtin, selenium_lib, ai_locator, browser_name)
                        logger.info(f"Successfully used Edge-compatible click for {ai_locator}")
                    else:
                        # For other keywords, try directly
                        builtin.run_keyword(keyword_name, ai_locator, *args)
                else:
                    # For non-Edge browsers, we'll still use enhanced operations but with browser-specific adaptations
                    keyword_lower = keyword_name.lower()
                    
                    if "input text" in keyword_lower or "type" in keyword_lower:
                        # Enhanced input text with browser-specific optimizations
                        self._enhanced_browser_input_text(builtin, selenium_lib, ai_locator, args, browser_name)
                        logger.info(f"Successfully used enhanced input for {ai_locator}")
                    elif "click" in keyword_lower:
                        # Enhanced click with browser-specific optimizations
                        self._enhanced_browser_click(builtin, selenium_lib, ai_locator, browser_name)
                        logger.info(f"Successfully used enhanced click for {ai_locator}")
                    else:
                        # For other keywords, try directly
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
    
    def _detect_browser_name(self, selenium_lib):
        """
        Detect the browser name from the Selenium WebDriver.
        
        :param selenium_lib: The SeleniumLibrary instance
        :return: Browser name string or None if detection fails
        """
        try:
            capabilities = selenium_lib.driver.capabilities
            return capabilities.get('browserName', '').lower()
        except Exception as e:
            logger.warn(f"Could not detect browser name: {e}")
            return None
    
    def _enhanced_browser_input_text(self, builtin, selenium_lib, locator, args, browser_name="unknown"):
        """
        Browser-adaptive input text operation that works across different browsers.
        
        :param builtin: BuiltIn instance
        :param selenium_lib: SeleniumLibrary instance
        :param locator: Element locator
        :param args: Keyword arguments (first arg should be the text to input)
        :param browser_name: Browser name for browser-specific optimizations
        """
        # Get the text to input
        text = args[0] if args else ""
        is_edge = browser_name and "edge" in browser_name.lower()
        
        # For Edge, start with Press Keys which often works better
        if is_edge:
            try:
                builtin.run_keyword("Press Keys", locator, text)
                return
            except Exception as e1:
                logger.warn(f"Press Keys failed in {browser_name}: {e1}")
        else:
            # For other browsers, try Input Text first which usually works best
            try:
                builtin.run_keyword("Input Text", locator, text)
                return
            except Exception as e1:
                logger.warn(f"Input Text failed in {browser_name}: {e1}")
        
        # Generic fallbacks for all browsers - try direct WebDriver methods
        try:
            # Try getting the element and using send_keys directly
            element = selenium_lib.find_element(locator)
            # Clear first for more reliable behavior
            try:
                element.clear()
            except:
                pass
            element.send_keys(text)
            return
        except Exception as e2:
            logger.warn(f"WebDriver send_keys failed in {browser_name}: {e2}")
        
        # JavaScript fallback - generally works across most browsers
        # but with different levels of reliability
        try:
            # Use a cross-browser compatible JS approach
            js_script = """
                (function(el, text) {
                    try {
                        // For input elements
                        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                            el.value = text;
                            
                            // Trigger events for framework detection
                            var inputEvent = document.createEvent('Event');
                            inputEvent.initEvent('input', true, true);
                            el.dispatchEvent(inputEvent);
                            
                            var changeEvent = document.createEvent('Event');
                            changeEvent.initEvent('change', true, true);
                            el.dispatchEvent(changeEvent);
                            
                            return true;
                        }
                        // For contenteditable
                        else if (el.isContentEditable) {
                            el.innerText = text;
                            return true;
                        }
                        return false;
                    } catch(e) {
                        return false;
                    }
                })(arguments[0], arguments[1]);
            """
            result = builtin.run_keyword("Execute JavaScript", js_script, locator, text)
            if result:
                return
        except Exception as e3:
            logger.warn(f"JavaScript input approach failed in {browser_name}: {e3}")
        
        # Last desperate attempt - the simplest possible JS approach
        builtin.run_keyword("Execute JavaScript", 
                          "arguments[0].value = arguments[1];", 
                          locator, text)
    
    def _enhanced_browser_click(self, builtin, selenium_lib, locator, browser_name="unknown"):
        """
        Browser-adaptive click operation that works across different browsers.
        
        :param builtin: BuiltIn instance
        :param selenium_lib: SeleniumLibrary instance
        :param locator: Element locator
        :param browser_name: Browser name for browser-specific optimizations
        """
        is_edge = browser_name and "edge" in browser_name.lower()
        
        # First try to scroll element into view - works across all browsers
        try:
            builtin.run_keyword_and_ignore_error("Execute JavaScript", 
                                               "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", 
                                               locator)
            
            # Allow some time for the scroll - especially important in Edge
            if is_edge:
                builtin.run_keyword("Sleep", "0.5s")
            else:
                builtin.run_keyword("Sleep", "0.2s")
        except:
            pass
        
        # For Edge, we need to be extra careful with visibility and interactability
        if is_edge:
            try:
                builtin.run_keyword_and_ignore_error("Wait Until Element Is Visible", locator, "2s")
                builtin.run_keyword_and_ignore_error("Wait Until Element Is Enabled", locator, "2s")
            except:
                pass
            
        # Try standard click - usually works in most browsers
        try:
            builtin.run_keyword("Click Element", locator)
            return
        except Exception as e1:
            logger.warn(f"Click Element failed in {browser_name}: {e1}")
        
        # JavaScript click - reliable across browsers but might not trigger all event handlers
        try:
            # Cross-browser compatible JavaScript click
            js_script = """
                (function(el) {
                    try {
                        // Try HTMLElement.prototype.click to avoid any private field issues
                        HTMLElement.prototype.click.call(el);
                        return true;
                    } catch(e) {
                        try {
                            // Create and dispatch a MouseEvent
                            var evt = document.createEvent('MouseEvents');
                            evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                            return el.dispatchEvent(evt);
                        } catch(e2) {
                            return false;
                        }
                    }
                })(arguments[0]);
            """
            result = builtin.run_keyword("Execute JavaScript", js_script, locator)
            if result:
                return
        except Exception as e2:
            logger.warn(f"JavaScript click failed in {browser_name}: {e2}")
        
        # Direct WebDriver click - different behavior across browsers
        try:
            element = selenium_lib.find_element(locator)
            element.click()
        except Exception as e3:
            # If all else fails, we'll try the simplest JavaScript click
            builtin.run_keyword("Execute JavaScript", "arguments[0].click();", locator)
    
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