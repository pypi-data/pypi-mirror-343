#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import os
import requests
import hashlib
import unicodedata
import string
from robot.api import logger

class AIProcessor:
    
    def __init__(self, api_key=None, api_url="https://api.openai.com/v1/chat/completions", model="gpt-4.1", transformation_cache_file=None):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.transformation_cache_file = transformation_cache_file or os.path.join(os.path.expanduser("~"), ".dom_retry_transformation_cache.json")
        self.transformation_cache = self._load_transformation_cache()
        self.max_chunk_size = 10000  
        self.max_chunks = 3  
        
    def _normalize_text(self, text):
        """
        Normalize text by:
        1. Converting to lowercase
        2. Removing accents (diacritics)
        3. Removing punctuation
        4. Collapsing whitespace
        """
        if not text or not isinstance(text, str):
            return ""
            
        # Lowercase and NFKD normalization to handle accents
        text = unicodedata.normalize('NFKD', text.lower())
        
        # Remove accents
        text = ''.join([c for c in text if not unicodedata.combining(c)])
        
        # Remove punctuation
        text = ''.join([c for c in text if c not in string.punctuation])
        
        # Collapse whitespace
        text = ' '.join(text.split())
        
        logger.debug(f"Normalized text: '{text}'")
        return text
    
    def _normalize_xpath_text_conditions(self, xpath):
        """
        Add normalize-space() to text conditions in XPath expressions for better whitespace handling.
        This only modifies the XPath structure, not the text content being matched.
        """
        if not xpath:
            return xpath
            
        text_pattern = r"text\(\)\s*=\s*(['\"])(.*?)\1"
        
        def add_normalize_space(match):
            quote = match.group(1)  # Capture the quote type (' or ")
            text = match.group(2)   # Capture the text content
            return f"normalize-space(text()) = {quote}{text}{quote}"
            
        contains_pattern = r"contains\(\s*text\(\)\s*,\s*(['\"])(.*?)\1\s*\)"
        
        def add_normalize_space_to_contains(match):
            quote = match.group(1)  # Capture the quote type (' or ")
            text = match.group(2)   # Capture the text content
            return f"contains(normalize-space(text()), {quote}{text}{quote})"
        
        normalized_xpath = re.sub(text_pattern, add_normalize_space, xpath)
        normalized_xpath = re.sub(contains_pattern, add_normalize_space_to_contains, normalized_xpath)
        
        if normalized_xpath != xpath:
            logger.info(f"Added normalize-space() to text conditions: '{xpath}' → '{normalized_xpath}'")
            
        return normalized_xpath
        
    def generate_locator(self, html, element_description, original_locator=None, page_url=None, selenium_lib=None):
        if not self.api_key:
            raise Exception("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        logger.info(f"Looking for element with description: '{element_description}'")
        logger.info(f"Using enhanced XPath strategy: Including 2-3 parent elements for more robust locators")
        
        if original_locator and element_description:
            desc_hash = hashlib.md5(element_description.encode()).hexdigest()[:8]
            cache_key = f"{original_locator}::{desc_hash}::{element_description}"
            
            cached_locator = self._check_transformation_cache(cache_key)
            if cached_locator:
                logger.info(f"Using cached transformation for '{element_description}': {original_locator} → {cached_locator}")
                return cached_locator
        
        html_chunks = self._split_html_into_chunks(html)
        
        # Try to find the element in each chunk
        for i, chunk in enumerate(html_chunks[:self.max_chunks]):
            logger.info(f"Trying HTML chunk {i+1}/{len(html_chunks[:self.max_chunks])}")
            try:
                ai_locator = self._call_openai_api(chunk, element_description, original_locator, 
                                                  chunk_info=f"chunk {i+1}/{len(html_chunks[:self.max_chunks])}")
                
                # Normalize 
                ai_locator = self._normalize_xpath_text_conditions(ai_locator)
                
                if ai_locator and ai_locator != "//*":
                    if original_locator and element_description:
                        desc_hash = hashlib.md5(element_description.encode()).hexdigest()[:8]
                        cache_key = f"{original_locator}::{desc_hash}::{element_description}"
                        self._store_transformation(cache_key, ai_locator)
                    logger.info(f"Successfully found locator for '{element_description}': {ai_locator}")
                    
                    # Count the number of parent elements in the path
                    parent_levels = ai_locator.count('/') - 1 if ai_locator.startswith('//') else ai_locator.count('/')
                    if parent_levels > 1:
                        logger.info(f"Enhanced locator includes {parent_levels} levels in path for better context and stability")
                    
                    return ai_locator
            except Exception as e:
                logger.warn(f"Error with chunk {i+1}: {e}")
                
        # If we get here, we tried all chunks and failed, try with a condensed version of the entire HTML
        try:
            logger.info(f"Trying with condensed full HTML for '{element_description}'")
            logger.info("Still generating an XPath with parent elements for better element context")
            condensed_html = self._extract_important_html_sections(html)
            ai_locator = self._call_openai_api(condensed_html, element_description, original_locator,
                                             chunk_info="condensed full HTML")
            
            # Normalize any text conditions in the XPath
            ai_locator = self._normalize_xpath_text_conditions(ai_locator)
            
            logger.info(f"Generated locator from condensed HTML for '{element_description}': {ai_locator}")
            
            # Count the number of parent elements in the path
            parent_levels = ai_locator.count('/') - 1 if ai_locator.startswith('//') else ai_locator.count('/')
            if parent_levels > 1:
                logger.info(f"Enhanced locator includes {parent_levels} levels in path for better context and stability")
        except Exception as e:
            logger.error(f"OpenAI API call failed with condensed HTML: {e}")
            ai_locator = "//*"  # Very basic 
            
        if original_locator and ai_locator and element_description:
            desc_hash = hashlib.md5(element_description.encode()).hexdigest()[:8]
            cache_key = f"{original_locator}::{desc_hash}::{element_description}"
            self._store_transformation(cache_key, ai_locator)
            
        return ai_locator

    def _split_html_into_chunks(self, html):
        """Split HTML into meaningful chunks for processing."""
        if not html:
            return [""]
            
        # First try to extract key sections
        chunks = []
        
        # Look for forms which often contain interactive elements
        forms = re.findall(r'<form[^>]*>.*?</form>', html, re.DOTALL)
        if forms:
            for form in forms:
                if len(form) > 500:  # Only include substantial forms
                    chunks.append(form)
        
        # Look for main content areas
        main_divs = re.findall(r'<(?:main|div[^>]*?(?:id|class)\s*=\s*["\'][^"\']*?(?:main|content|container)[^"\']*?["\'])[^>]*>.*?</(?:main|div)>', html, re.DOTALL)
        if main_divs:
            for div in main_divs:
                if len(div) > 1000:  # Only include substantial content areas
                    chunks.append(div)
        
        # Add navigation elements separately
        nav_elements = re.findall(r'<(?:nav|header)[^>]*>.*?</(?:nav|header)>', html, re.DOTALL)
        if nav_elements:
            chunks.extend(nav_elements)
        
        # If we found meaningful chunks, use them
        if chunks:
            # If any chunk is too large, truncate it
            for i in range(len(chunks)):
                if len(chunks[i]) > self.max_chunk_size:
                    chunks[i] = chunks[i][:self.max_chunk_size]
            return chunks
            
        # Fallback: just split the HTML into equal chunks
        if len(html) > self.max_chunk_size:
            # Calculate number of chunks needed
            num_chunks = (len(html) + self.max_chunk_size - 1) // self.max_chunk_size
            return [html[i*self.max_chunk_size:(i+1)*self.max_chunk_size] for i in range(num_chunks)]
        
        return [html]
    
    def _extract_important_html_sections(self, html):
        """Extract and condense the most important parts of the HTML."""
        if not html:
            return ""
            
        condensed = []
        
        # Extract all element tags with id or class attributes
        important_elements = re.findall(r'<[^>]*(?:id|class)\s*=\s*["\'][^"\']*["\'][^>]*>', html)
        condensed.extend(important_elements[:500])  # Limit to 500 elements
        
        # Extract all interactive elements (buttons, inputs, etc.)
        interactive = re.findall(r'<(?:button|input|select|textarea|a)[^>]*>.*?</(?:button|input|select|textarea|a)>', html, re.DOTALL)
        condensed.extend(interactive[:300])  # Limit to 300 elements
        
        result = "".join(condensed)
        if not result:
            # If we couldn't extract anything useful, return a truncated version of the HTML
            return html[:self.max_chunk_size]
            
        return result[:self.max_chunk_size]  # Make sure we don't exceed the max size

    def _simple_preprocess_html(self, html):
        if not html:
            return ""
            
        # Remove scripts and styles to reduce noise
        html = re.sub(r'<script\b[^<]*(?:(?!</script>)<[^<]*)*</script>', '', html)
        html = re.sub(r'<style\b[^<]*(?:(?!</style>)<[^<]*)*</style>', '', html)
        
        return html
            
    def _call_openai_api(self, html, description, original_locator=None, chunk_info=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        system_message = f"""You are a web automation expert that helps find XPath selectors for web elements.
You MUST return a syntactically correct XPath selector that follows XPath specification.
ONLY return the raw XPath expression, nothing else - no explanations, no markdown formatting, no prefix.

IMPORTANT: Your task is to find an element that matches EXACTLY this description: "{description}"
Focus specifically on this description and ignore any other prominent elements unless they match this description.

ABSOLUTELY CRITICAL: ALWAYS USE '//' BETWEEN ALL ELEMENTS in your XPath. NEVER use direct '/' paths.
For example, instead of "//div[@class='form']/div[@class='field']/input", 
ALWAYS use "//div[@class='form']//div[@class='field']//input"

This is critical because modern web apps often have dynamic structures with hidden divs, forms, or other elements 
that might be inserted between parent and child elements.

CRITICAL REQUIREMENT: Your XPath MUST include 2-3 levels of parent elements above the target element to create a more robust locator.
For example, instead of returning "//button[@id='submit']", return something like "//div[@class='form-group']//div[@class='button-container']//button[@id='submit']"

Rules for creating valid XPath selectors:
1. NEVER include any prefix like 'xpath=' - return only the raw XPath expression starting with '//'
2. Ensure all brackets [] are properly balanced
3. Ensure all parentheses () are properly balanced
4. Always use single or double quotes consistently for attribute values
5. Use only valid XPath axes (e.g., ancestor, descendant, following-sibling)
6. Make sure predicates [condition] are properly formed with correct operators
7. Properly escape quotes inside attribute values
8. Use XPath functions like contains(), text(), and starts-with() properly
9. Make selectors as specific as possible to uniquely identify elements
10. Consider using multiple attributes when needed (e.g., [@id='xyz' and @class='abc'])
11. When targeting text content, use text() functions correctly
12. ALWAYS include 2-3 parent elements in your XPath for robustness and context
13. MANDATORY: ALWAYS use '//' between ALL elements. NEVER use direct '/' path separators.
   - INCORRECT: //div[@class='parent']/span[@class='child']
   - CORRECT: //div[@class='parent']//span[@class='child']
   - This rule is absolutely critical for handling complex DOM structures with nested forms, divs, etc.

THE MOST IMPORTANT THING: The element you find MUST match the description: "{description}" - not other visible elements.
Return ONLY the raw XPath expression with no prefix or additional text."""
        
        user_message = f"""I need a precise XPath selector for the element described as: "{description}"\n\n"""
        
        if original_locator:
            # Strip prefix if present in the original locator
            stripped_locator = original_locator
            if original_locator.startswith("xpath="):
                stripped_locator = original_locator[6:]
            user_message += f"""The original XPath "{stripped_locator}" didn't work.\n\n"""
            
        if chunk_info:
            user_message += f"""I'm providing {chunk_info} of the HTML.\n\n"""
            
        user_message += f"""Here's the HTML:\n\n{html}\n\n"""
        
        user_message += f"""Return ONLY the raw XPath expression for the element described as: "{description}" without any prefix.
Make sure the selector is specific to this exact description and not other prominent elements on the page.

IMPORTANT: Create an XPath that includes 2-3 levels of parent elements above the target element. 
This provides better context and makes the selector more robust.
For example: "//section[@class='main-content']//div[@class='user-panel']//button[contains(text(), 'Submit')]"

ABSOLUTELY MANDATORY - Use '//' between ALL elements in your XPath:
- ALWAYS use the '//' path separator between ALL parent and child elements
- NEVER use the direct '/' path separator as it won't work with nested elements
- INCORRECT: //div[@class='parent']/span[@class='child']
- CORRECT: //div[@class='parent']//span[@class='child']
- This is critical for handling forms, nested divs, and other complex DOM structures

Follow these validation steps before returning your answer:
1. Double-check that all brackets [] and parentheses () are properly balanced
2. Verify that all quotes are properly paired and escaped
3. Confirm that all XPath functions and axes are correctly used
4. Ensure predicates are properly formed with correct operators
5. Check that attribute selectors are valid and use proper XPath syntax
6. Remove any whitespace, newlines, or stray characters from the final selector
7. Ensure your answer starts with '//' and NOT with 'xpath='
8. VERIFY that your selector matches the description: "{description}"
9. CONFIRM that your XPath includes 2-3 parent elements above the target element
10. CONFIRM that ALL elements are connected with '//' and NEVER with direct '/'

YOUR RESPONSE MUST BE A SINGLE LINE CONTAINING ONLY THE RAW XPATH EXPRESSION."""

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
            
            if selector.startswith('```') and selector.endswith('```'):
                selector = selector[3:-3].strip()
            
            selector = selector.replace('\n', '').replace('\r', '')
            
            if selector.startswith('xpath='):
                selector = selector[6:]
                
            # Make sure the selector starts with / or //
            if not (selector.startswith('/') or selector.startswith('//')):
                selector = f"//{selector}"
                
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