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
        self.max_chunk_size = 10000  # Maximum size of HTML chunk to send to API
        self.max_chunks = 3  # Maximum number of chunks to try
        
    def generate_locator(self, html, element_description, original_locator=None, page_url=None, selenium_lib=None):
        if not self.api_key:
            raise Exception("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        if original_locator and element_description:
            cache_key = f"{original_locator}::{element_description}"
            cached_locator = self._check_transformation_cache(cache_key)
            if cached_locator:
                logger.info(f"Using cached transformation for {element_description}: {original_locator} → {cached_locator}")
                return cached_locator
        
        html_chunks = self._split_html_into_chunks(html)
        
        # Try to find the element in each chunk
        for i, chunk in enumerate(html_chunks[:self.max_chunks]):
            logger.info(f"Trying HTML chunk {i+1}/{len(html_chunks[:self.max_chunks])}")
            try:
                ai_locator = self._call_openai_api(chunk, element_description, original_locator, 
                                                  chunk_info=f"chunk {i+1}/{len(html_chunks[:self.max_chunks])}")
                
                # If we got a valid response, store and return it
                if ai_locator and ai_locator != "css=body *":
                    if original_locator and element_description:
                        cache_key = f"{original_locator}::{element_description}"
                        self._store_transformation(cache_key, ai_locator)
                    return ai_locator
            except Exception as e:
                logger.warn(f"Error with chunk {i+1}: {e}")
                
        # If we get here, we tried all chunks and failed, try with a condensed version of the entire HTML
        try:
            logger.info("Trying with condensed full HTML")
            condensed_html = self._extract_important_html_sections(html)
            ai_locator = self._call_openai_api(condensed_html, element_description, original_locator,
                                             chunk_info="condensed full HTML")
        except Exception as e:
            logger.error(f"OpenAI API call failed with condensed HTML: {e}")
            ai_locator = "css=body *"  # Very basic fallback
            
        if original_locator and ai_locator and element_description:
            cache_key = f"{original_locator}::{element_description}"
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

        system_message = """You are a web automation expert that helps find CSS or XPath selectors for web elements.
You MUST return a syntactically correct selector that follows CSS or XPath specification.
ONLY return the selector, nothing else - no explanations, no markdown formatting.

Rules for creating valid CSS selectors:
1. Always start with 'css=' prefix
2. Ensure all brackets [] are properly balanced and contain valid attributes
3. Ensure all parentheses () are properly balanced
4. Quotes inside attribute selectors must be properly escaped or balanced
5. Avoid complex pseudo-selectors like :has() or :contains() that aren't universally supported
6. Prefer simple selectors using id (#id) or class (.class) when possible
7. Always check that special characters are properly escaped

Rules for creating valid XPath selectors:
1. Always start with 'xpath=' prefix 
2. Ensure all brackets [] are properly balanced
3. Ensure all parentheses () are properly balanced
4. Always use single or double quotes consistently for attribute values
5. Use only valid XPath axes (e.g., ancestor, descendant, following-sibling)
6. Make sure predicates [condition] are properly formed with correct operators
7. Properly escape quotes inside attribute values

MOST IMPORTANT: Return ONLY the selector string with no other text."""
        
        user_message = f"""I need a precise CSS or XPath selector for: "{description}"\n\n"""
        
        if original_locator:
            user_message += f"""The original locator "{original_locator}" didn't work.\n\n"""
            
        if chunk_info:
            user_message += f"""I'm providing {chunk_info} of the HTML.\n"""
            
        user_message += f"""Here's the HTML:\n\n{html}\n\n"""
        
        user_message += """Return ONLY the selector as a raw string with the appropriate prefix (css= or xpath=).
Make sure the selector is as specific and accurate as possible.

Follow these validation steps before returning your answer:
1. Double-check that all brackets [] and parentheses () are properly balanced
2. Verify that all quotes are properly paired and escaped
3. Confirm that attribute selectors are properly formed
4. For XPath, ensure all axes and predicates are syntactically correct
5. For CSS, make sure attribute selectors follow the correct syntax
6. Remove any whitespace, newlines, or stray characters from the final selector

YOUR RESPONSE MUST BE A SINGLE LINE CONTAINING ONLY THE SELECTOR."""

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