#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import traceback
from robot.api import logger
from robot.api.deco import keyword
from dotenv import load_dotenv

from .ai_processor import AIProcessor
from .locator_manager import LocatorManager
from .keyword_handler import KeywordHandler

class DomRetryLibrary:
    """
    A Robot Framework library that provides a generic AI fallback mechanism
    for locator variables within utility keywords.

    This library enhances test reliability by using OpenAI to dynamically
    generate element locators when the primary locators fail.

    == Table of Contents ==

    - `Introduction`
    - `Installation`
    - `Usage`
    - `API Key Setup`
    - `Examples`
    - `Keywords`

    = Introduction =

    DomRetryLibrary leverages OpenAI's API to dynamically generate locators for web elements
    when the primary locators fail. This helps maintain test stability even when the UI changes.

    = Installation =

    Install the library using pip:
    | pip install robotframework-domretrylibrary

    = Usage =

    Import the library in your Robot Framework test file:
    | Library    DomRetryLibrary

    Define your locators and AI fallback descriptions:
    | *** Variables ***
    | ${USERNAME_FIELD}      css=#non_existent_username_id
    | ${AI_USERNAME_FIELD}   the username input field with placeholder 'Username'

    Use the AI fallback in your tests:
    | AI Fallback Locator    Input Text    USERNAME_FIELD    ${USERNAME}
    
    Or provide the AI description directly without needing an AI_ variable:
    | AI Fallback Locator    Input Text    css=#non_existent_id    ${USERNAME}    ai_description=the username input field
    
    = Support for Existing Test Structures (v2.4.0+) =
    
    The library can work with existing patterns like:
    
    | *** Keywords ***
    | Wait And Input Text
    |     [Arguments]    ${locator}    ${text}
    |     ${status}    ${error}=    Run Keyword And Ignore Error    Input Text    ${locator}    ${text}
    |     Run Keyword If    '${status}' == 'FAIL'    AI Fallback Locator    Input Text    ${locator}    ${text}
    
    = Enhanced Element Interaction (v2.5.0+) =
    
    The library now has enhanced element interaction capabilities to handle common Selenium issues:
    
    - Automatically retries failed interactions (up to 3 times)
    - Scrolls elements into view before interaction
    - Waits for elements to be visible and enabled
    - Falls back to JavaScript execution for input and click operations
    - Handles invalid element state exceptions automatically
    
    This means the library can work around many common Selenium issues like:
    - Elements that are not interactable due to being obscured
    - Elements that are technically in the DOM but not fully rendered
    - Elements in iframes or shadow DOMs
    - Elements with complex event handlers
    
    = Enhanced AI Processor (v2.5.0+) =
    
    Version 2.5.0 introduces significant improvements to the AI processor component:
    
    - Multi-strategy locator generation with three approaches (standard, precision, robust)
    - Smart caching system that remembers successful transformations 
    - Intelligent use of original locator as context for better alternatives
    - Element type classification for more targeted locators
    - Improved HTML preprocessing with focus on relevant page sections
    - Better element interaction with automatic scrolling and JavaScript fallbacks

    = API Key Setup =

    Store your OpenAI API key in a .env file or provide it when initializing the library:
    | Library    DomRetryLibrary    api_key=${OPENAI_API_KEY}

    = Examples =

    == Basic Usage Example ==

    | *** Settings ***
    | Library           SeleniumLibrary
    | Library           DomRetryLibrary
    |
    | *** Variables ***
    | ${USERNAME_FIELD}     css=#non_existent_username_id
    | ${AI_USERNAME_FIELD}  the username input field with placeholder 'Username'
    |
    | *** Test Cases ***
    | Login Test
    |     Open Browser    https://example.com    chrome
    |     AI Fallback Locator    Input Text    USERNAME_FIELD    myusername
    |     Close Browser
    
    == Direct Description Example ==
    
    | *** Settings ***
    | Library           SeleniumLibrary
    | Library           DomRetryLibrary
    |
    | *** Test Cases ***
    | Login Test
    |     Open Browser    https://example.com    chrome
    |     AI Fallback Locator    Input Text    css=#username    myusername    ai_description=the username input field
    |     Close Browser
    
    == Custom Keyword Example ==
    
    | *** Keywords ***
    | Wait And Input Text
    |     [Arguments]    ${locator}    ${text}
    |     ${status}    ${error}=    Run Keyword And Ignore Error    Input Text    ${locator}    ${text}
    |     Run Keyword If    '${status}' == 'FAIL'    AI Fallback Locator    Input Text    ${locator}    ${text}

    = Keywords =

    This library provides the following keywords:

    - `AI Fallback Locator` - Add AI fallback to any locator-based keyword
    - `Clear Locator History` - Clear the stored locator comparison history
    """

    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LIBRARY_VERSION = '2.5.1'
    ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'

    def __init__(self, openai_api_url="https://api.openai.com/v1/chat/completions", api_key=None, model="gpt-4o", locator_storage_file="locator_comparison.json", transformation_cache_file=None):
        """
        Initialize the DomRetryLibrary.

        :param openai_api_url: OpenAI API endpoint URL
        :param api_key: API key for OpenAI service (optional, will use environment variable if not provided)
        :param model: OpenAI model to use (default: gpt-4o)
        :param locator_storage_file: File to store locator comparison data
        :param transformation_cache_file: File to store transformation cache data (default: ~/.dom_retry_transformation_cache.json)
        """
        try:
            # Load environment variables from .env file
            load_dotenv()

            # Set API key (prioritize constructor parameter, fallback to environment variable)
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')

            if not self.api_key:
                logger.warn("No OpenAI API key provided. AI fallback will not work properly!")
            else:
                # Only show part of the API key for security
                masked_key = self.api_key[:7] + "..." + self.api_key[-4:] if len(self.api_key) > 11 else "***masked***"
                logger.info(f"Using OpenAI API key with format: {masked_key}")

            # Initialize the component modules
            self.ai_processor = AIProcessor(api_key=self.api_key, api_url=openai_api_url, model=model, transformation_cache_file=transformation_cache_file)
            self.locator_manager = LocatorManager(locator_storage_file=locator_storage_file)
            self.keyword_handler = KeywordHandler(self.ai_processor, self.locator_manager)

        except Exception as e:
            logger.error(f"Error initializing DomRetryLibrary: {str(e)}")
            logger.debug(traceback.format_exc())
            raise

    @keyword(name="AI Fallback Locator")
    def ai_fallback_locator(self, keyword_name, locator_var, *args, ai_description=None):
        """
        Add AI fallback to any locator-based keyword.
        
        This keyword will first try to use the primary locator, and if it fails,
        it will use the AI-generated locator as a fallback.
        
        Examples:
        | AI Fallback Locator | Input Text | USERNAME_FIELD | myusername |
        | AI Fallback Locator | Input Text | css=#username | myusername | ai_description=the username input field |
        
        In v2.4.0+, this keyword is more forgiving and will:
        - Handle empty locators by inferring from context
        - Try to find any matching AI_ variable if none is specified
        - Continue execution rather than failing when no description is found
        
        :param keyword_name: The keyword to execute (e.g., Input Text, Click Element)
        :param locator_var: Variable name or locator value 
        :param args: Additional arguments for the keyword
        :param ai_description: Optional AI description to use directly instead of looking up AI_ variables
        """
        return self.keyword_handler.ai_fallback_locator(keyword_name, locator_var, *args, ai_description=ai_description)

    @keyword
    def clear_locator_history(self):
        """
        Clear the stored locator comparison history.
        
        Example:
        | Clear Locator History |
        """
        self.locator_manager.clear_history()



