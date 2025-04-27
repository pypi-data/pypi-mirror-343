#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import os
import requests
from robot.api import logger

class AIProcessor:
    
    def __init__(self, api_key=None, api_url="https://api.openai.com/v1/chat/completions", model="gpt-4o", transformation_cache_file=None):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.transformation_cache_file = transformation_cache_file or os.path.join(os.path.expanduser("~"), ".dom_retry_transformation_cache.json")
        self.transformation_cache = self._load_transformation_cache()
        
    def generate_locator(self, html, element_description, original_locator=None, page_url=None, selenium_lib=None):
        if not self.api_key:
            raise Exception("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        if original_locator and element_description:
            cache_key = f"{original_locator}::{element_description}"
            cached_locator = self._check_transformation_cache(cache_key)
            if cached_locator:
                logger.info(f"Using cached transformation for {element_description}: {original_locator} → {cached_locator}")
                return cached_locator
        
        html = self._simple_preprocess_html(html)
        
        try:
            ai_locator = self._call_openai_api(html, element_description, original_locator)
            # Validate the selector
            if not self._is_valid_selector(ai_locator):
                logger.warn(f"AI generated an invalid selector: {ai_locator}. Using fallback.")
                ai_locator = self.derive_simple_locator(element_description)
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            ai_locator = self.derive_simple_locator(element_description)
            
        if original_locator and ai_locator and element_description:
            cache_key = f"{original_locator}::{element_description}"
            self._store_transformation(cache_key, ai_locator)
            
        return ai_locator
        
    def derive_simple_locator(self, description):
        description = description.lower()
        
        if "password" in description:
            return "css=input[type='password']"
        elif "button" in description or "submit" in description or "click" in description:
            return "css=button, input[type='submit'], input[type='button'], .btn, .button"
        elif "username" in description or "email" in description or "input" in description:
            return "css=input[type='text'], input:not([type]), input[type='email']"
        else:
            words = [w for w in description.split() if len(w) > 3]
            if words:
                key_word = words[0]
                return f"css=[id*='{key_word}'], [name*='{key_word}'], [class*='{key_word}']"
            return "css=button, .btn, .button"  # More generic fallback than just login button

    def _is_valid_selector(self, selector):
        """Check if a selector is syntactically valid."""
        if not selector:
            return False
            
        if selector.startswith('css='):
            css_selector = selector[4:]
            # Basic CSS selector validation
            try:
                # Check for unbalanced brackets, quotes, or parentheses
                if css_selector.count('[') != css_selector.count(']'):
                    return False
                if css_selector.count('(') != css_selector.count(')'):
                    return False
                if css_selector.count("'") % 2 != 0 or css_selector.count('"') % 2 != 0:
                    return False
                # Check for common syntax errors
                if '::' in css_selector and not any(pseudo in css_selector for pseudo in ['::before', '::after', '::first-line', '::first-letter']):
                    return False
                return True
            except:
                return False
        elif selector.startswith('xpath='):
            xpath_selector = selector[6:]
            # Basic XPath selector validation
            try:
                # Check for unbalanced brackets, quotes, or parentheses
                if xpath_selector.count('[') != xpath_selector.count(']'):
                    return False
                if xpath_selector.count('(') != xpath_selector.count(')'):
                    return False
                if xpath_selector.count("'") % 2 != 0 or xpath_selector.count('"') % 2 != 0:
                    return False
                return True
            except:
                return False
        return False

    def _simple_preprocess_html(self, html):
        if not html:
            return ""
            
        # Truncate large HTML to avoid token limits
        max_length = 8000
        if len(html) > max_length:
            html = html[:max_length]
            
        return html
            
    def _call_openai_api(self, html, description, original_locator=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        system_message = "You are a web automation expert that helps find CSS or XPath selectors for web elements. You MUST return a syntactically correct selector that follows CSS or XPath specification."
        
        user_message = f"""Given the following HTML, provide a CSS selector or XPath that precisely identifies the element described as: "{description}". """
        
        if original_locator:
            user_message += f"""The original locator "{original_locator}" failed to locate the element."""
        
        user_message += f"""
Return ONLY the selector as a raw string, without any explanation, quotes, or formatting.
IMPORTANT: Make sure your selector is syntactically valid. For CSS, check that brackets and quotes are balanced.
For XPath, ensure proper axis notation and predicate syntax.

HTML:
{html}
"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 250,
        }

        response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"API returned error: {response.status_code} - {response.text}")
            
        data = response.json()
        
        if 'choices' in data and len(data['choices']) > 0:
            selector = data['choices'][0]['message']['content'].strip()
            
            # Remove markdown formatting if present
            if selector.startswith('```') and selector.endswith('```'):
                selector = selector[3:-3].strip()
            
            # Clean up the selector
            selector = selector.replace('\n', '').replace('\r', '')
            
            # Add prefix if missing
            if selector.startswith('//'):
                selector = f"xpath={selector}"
            elif not (selector.startswith('css=') or selector.startswith('xpath=')):
                selector = f"css={selector}"
                
            return selector
        else:
            raise Exception(f"No valid response from OpenAI API: {data}")
    
    def _load_transformation_cache(self):
        if not os.path.exists(self.transformation_cache_file):
            return {}
        
        try:
            with open(self.transformation_cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warn(f"Error loading transformation cache: {e}")
            return {}
    
    def _save_transformation_cache(self):
        try:
            with open(self.transformation_cache_file, 'w') as f:
                json.dump(self.transformation_cache, f)
        except Exception as e:
            logger.warn(f"Error saving transformation cache: {e}")
    
    def _check_transformation_cache(self, cache_key):
        if cache_key in self.transformation_cache:
            return self.transformation_cache[cache_key]
        return None
    
    def _store_transformation(self, cache_key, transformed_locator):
        self.transformation_cache[cache_key] = transformed_locator
        self._save_transformation_cache()
        logger.info(f"Stored transformation for key '{cache_key}': {transformed_locator}") 