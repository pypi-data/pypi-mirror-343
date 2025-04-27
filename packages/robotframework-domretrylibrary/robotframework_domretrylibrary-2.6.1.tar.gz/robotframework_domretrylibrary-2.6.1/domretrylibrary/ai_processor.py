#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import os
import requests
from robot.api import logger

class AIProcessor:
    """
    Handles AI processing functions for DOM element locator generation.
    """
    
    def __init__(self, api_key=None, api_url="https://api.openai.com/v1/chat/completions", model="gpt-4o", transformation_cache_file=None):
        """
        Initialize the AI processor.
        
        :param api_key: OpenAI API key
        :param api_url: OpenAI API endpoint URL
        :param model: OpenAI model to use
        :param transformation_cache_file: File to store transformation cache data
        """
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.transformation_cache_file = transformation_cache_file or os.path.join(os.path.expanduser("~"), ".dom_retry_transformation_cache.json")
        self.transformation_cache = self._load_transformation_cache()
        
    def generate_locator(self, html, element_description, original_locator=None, page_url=None, selenium_lib=None):
        """
        Generate a locator for an element based on its description.
        
        :param html: HTML content of the page
        :param element_description: Natural language description of the element
        :param original_locator: The original locator that failed (optional)
        :param page_url: The URL of the page (optional)
        :param selenium_lib: SeleniumLibrary instance for additional context (optional)
        :return: AI-generated locator
        """
        if not self.api_key:
            raise Exception("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Check transformation cache first if we have the original locator
        if original_locator:
            cached_locator = self._check_transformation_cache(original_locator)
            if cached_locator:
                logger.info(f"Using cached transformation: {original_locator} → {cached_locator}")
                return cached_locator
        
        # Process the HTML to reduce its size
        processed_html = self._preprocess_html(html)
        
        if not processed_html:
            raise ValueError("No HTML content to analyze after preprocessing")
        
        # Try multiple strategies in order
        ai_locator = self._multi_strategy_locator_generation(
            processed_html, 
            element_description, 
            original_locator,
            page_url, 
            selenium_lib
        )
        
        # If we have the original locator, store the transformation
        if original_locator and ai_locator:
            self._store_transformation(original_locator, ai_locator)
            
        return ai_locator
        
    def derive_contextual_locator(self, html, description, original_locator=None):
        """
        Derive a basic locator from context when API is unavailable.
        This is a fallback method used when the API call fails.
        
        :param html: HTML content
        :param description: Element description
        :param original_locator: The original locator that failed (optional)
        :return: A context-derived locator
        """
        try:
            description = description.lower()
            element_type = self._classify_element_type(description, original_locator)

            if element_type == "text_input":
                return "css=input[type='text'], input:not([type]), input[placeholder*='user'], input.username"
            elif element_type == "password":
                return "css=input[type='password']"
            elif element_type == "button":
                return "css=button, input[type='submit'], input[type='button'], .btn, .button, a.btn, a.button"
            elif element_type == "checkbox":
                return "css=input[type='checkbox']"
            elif element_type == "radio":
                return "css=input[type='radio']"
            elif element_type == "select":
                return "css=select"
            elif element_type == "link":
                # Try to find links containing key terms from the description
                key_terms = [term for term in description.split() if len(term) > 3]
                if key_terms:
                    terms_selector = ', '.join([f"a:contains('{term}')" for term in key_terms])
                    return f"css={terms_selector}"
                return "css=a"
            elif element_type == "product":
                return "css=.product, .product-item, .inventory_item, .item"
            else:
                # Default more intelligent fallback based on description keywords
                keywords = [word for word in description.lower().split() if len(word) > 3]
                selectors = []
                
                # Build potential selectors from description keywords
                for keyword in keywords:
                    selectors.extend([
                        f"[id*='{keyword}']",
                        f"[class*='{keyword}']",
                        f"[name*='{keyword}']",
                        f"[placeholder*='{keyword}']",
                        f"[title*='{keyword}']",
                        f"[aria-label*='{keyword}']",
                        f"[data-test*='{keyword}']",
                        f"[data-testid*='{keyword}']"
                    ])
                
                # If we have original locator, try to get some parts from it
                if original_locator:
                    if original_locator.startswith('css='):
                        # Try to extract meaningful parts from the CSS selector
                        css_parts = original_locator[4:].split()
                        for part in css_parts:
                            # Extract classes or IDs
                            if '.' in part or '#' in part:
                                selectors.append(part)
                    elif original_locator.startswith('xpath='):
                        # For XPath, we'll just use some general selectors
                        selectors.extend(["input", "button", "a", "select"])
                
                # Join all selectors with commas for a CSS selector
                if selectors:
                    return f"css={', '.join(selectors)}"
                
                # Ultimate fallback
                return "css=body"
        except Exception as e:
            logger.error(f"Error deriving context locator: {str(e)}")
            # Fallback to a very generic locator
            return "css=body"

    def _preprocess_html(self, html, max_length=8000):
        """
        Preprocess HTML to reduce size before sending to OpenAI.

        :param html: Full HTML content
        :param max_length: Maximum length of processed HTML
        :return: Processed HTML
        """
        try:
            # Safety check for None or empty HTML
            if not html:
                logger.warn("Empty HTML provided for preprocessing")
                return ""
                
            # Remove scripts and styles
            html = re.sub(r'<script\b[^<]*(?:(?!</script>)<[^<]*)*</script>', '', html)
            html = re.sub(r'<style\b[^<]*(?:(?!</style>)<[^<]*)*</style>', '', html)

            # Remove HTML comments
            html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

            # Remove SVG elements (often large and not relevant for locators)
            html = re.sub(r'<svg\b[^<]*(?:(?!</svg>)<[^<]*)*</svg>', '', html, flags=re.DOTALL)

            # Remove hidden elements
            html = re.sub(r'<[^>]*?style\s*=\s*["\'][^"\']*?(display:\s*none|visibility:\s*hidden)[^"\']*?["\'][^>]*>.*?</[^>]*>', '', html, flags=re.DOTALL)

            # Focus on body content if possible
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
            if body_match:
                html = body_match.group(1)

            # More intelligent filtering - extract main content areas
            content_areas = []
            
            # Find main content containers
            main_divs = re.findall(r'<(?:main|div[^>]*?(?:id|class)\s*=\s*["\'][^"\']*?(?:main|content|container)[^"\']*?["\'])[^>]*>(.*?)</(?:main|div)>', html, re.DOTALL)
            if main_divs:
                # Use the longest main div as it likely contains the most content
                main_content = max(main_divs, key=len)
                content_areas.append(main_content)
            
            # Find forms
            forms = re.findall(r'<form[^>]*>(.*?)</form>', html, re.DOTALL)
            if forms:
                content_areas.extend(forms)
                
            # If we found content areas, use them instead of full HTML
            if content_areas and sum(len(area) for area in content_areas) > 100:  # Minimum sensible size
                html = ''.join(content_areas)
            
            # Truncate if still too long
            if len(html) > max_length:
                html = html[:max_length]

            return html
        except Exception as e:
            logger.warn(f"HTML preprocessing failed: {e}. Using truncated HTML.")
            return html[:max_length] if html and len(html) > max_length else ""
            
    def _call_openai_api(self, html, description, original_locator=None, approach="standard"):
        """
        Call the OpenAI API to get a locator based on the description.

        :param html: Preprocessed HTML content
        :param description: Natural language description of the element
        :param original_locator: The original locator that failed (optional)
        :param approach: The approach to use for generating the locator
        :return: AI-generated locator
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # Build the system message based on the approach
        system_message = "You are a web automation expert that helps find CSS or XPath selectors for web elements."
        if approach == "precision":
            system_message += " You generate extremely precise and unique selectors."
        elif approach == "robust":
            system_message += " You create robust selectors that can withstand minor UI changes."
        
        # Build the user message based on the approach and available context
        user_message = f"""Given the following HTML, provide a CSS selector or XPath that precisely identifies the element described as: "{description}". """
        
        # Include original locator as context if available
        if original_locator and approach != "ignore_original":
            user_message += f"""
            
The original locator "{original_locator}" failed to locate the element. Use this as context but create a completely new, improved locator.
            """
        
        user_message += f"""
Return ONLY the selector as a raw string, without any explanation, quotes, or formatting.

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
            "temperature": 0.1,  # Lower temperature for more deterministic results
            "max_tokens": 250,
        }

        logger.debug(f"Calling OpenAI API with model: {self.model} (approach: {approach})")

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)

            # Log response status and headers for debugging
            logger.debug(f"API Response Status: {response.status_code}")

            if response.status_code == 401:
                logger.error("API authentication failed. Please check your API key.")
                raise Exception("API authentication failed with 401 Unauthorized")

            response.raise_for_status()
            data = response.json()

            if 'choices' in data and len(data['choices']) > 0:
                selector = data['choices'][0]['message']['content'].strip()
                # Add css= or xpath= prefix if not present
                if selector.startswith('//'):
                    selector = f"xpath={selector}"
                elif not (selector.startswith('css=') or selector.startswith('xpath=')):
                    selector = f"css={selector}"
                return selector
            else:
                logger.error(f"Unexpected API response format: {data}")
                raise Exception(f"No valid response from OpenAI API: {data}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            raise
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _multi_strategy_locator_generation(self, html, description, original_locator=None, page_url=None, selenium_lib=None):
        """
        Use multiple strategies to generate locators, trying them in order of complexity.
        
        :param html: The preprocessed HTML
        :param description: The element description
        :param original_locator: The original locator that failed
        :param page_url: The URL of the page
        :param selenium_lib: SeleniumLibrary instance
        :return: The best locator found
        """
        logger.info(f"Using multi-strategy approach to generate locator for: {description}")
        
        # Strategy 1: Standard approach with original locator as context
        try:
            logger.info("Trying standard approach with original locator context")
            locator = self._call_openai_api(html, description, original_locator, approach="standard")
            return locator
        except Exception as e:
            logger.warn(f"Standard approach failed: {e}")
        
        # Strategy 2: Precision approach (ignoring original locator)
        try:
            logger.info("Trying precision approach without original locator")
            locator = self._call_openai_api(html, description, None, approach="precision")
            return locator
        except Exception as e:
            logger.warn(f"Precision approach failed: {e}")
        
        # Strategy 3: Robust approach for fallback
        try:
            logger.info("Trying robust approach")
            locator = self._call_openai_api(html, description, original_locator, approach="robust")
            return locator
        except Exception as e:
            logger.warn(f"Robust approach failed: {e}")
        
        # Fallback: Pattern-based locator generation
        logger.info("Using pattern-based fallback generation")
        return self.derive_contextual_locator(html, description, original_locator)
    
    def _classify_element_type(self, description, original_locator=None):
        """
        Classify the type of element being sought to improve locator generation.
        
        :param description: The element description
        :param original_locator: The original locator that failed
        :return: Element type classification
        """
        description_lower = description.lower()
        
        # Classification based on original locator
        if original_locator:
            if "password" in original_locator.lower():
                return "password"
            elif "checkbox" in original_locator.lower() or "check" in original_locator.lower():
                return "checkbox"
            elif "radio" in original_locator.lower():
                return "radio"
            elif "select" in original_locator.lower() or "dropdown" in original_locator.lower():
                return "select"
            elif "button" in original_locator.lower() or "btn" in original_locator.lower():
                return "button"
            elif "link" in original_locator.lower():
                return "link"
            
        # Classification based on description
        if "password" in description_lower:
            return "password"
        elif "check" in description_lower or "checkbox" in description_lower:
            return "checkbox"
        elif "radio" in description_lower:
            return "radio"
        elif "select" in description_lower or "dropdown" in description_lower or "drop down" in description_lower or "drop-down" in description_lower:
            return "select"
        elif "button" in description_lower or "submit" in description_lower or "click" in description_lower:
            return "button"
        elif "link" in description_lower or "anchor" in description_lower:
            return "link"
        elif "username" in description_lower or "user name" in description_lower or "email" in description_lower or "text field" in description_lower or "input field" in description_lower:
            return "text_input"
        elif "product" in description_lower or "item" in description_lower or "inventory" in description_lower:
            return "product"
            
        # Default
        return "generic"
    
    def _load_transformation_cache(self):
        """
        Load the transformation cache from disk.
        
        :return: Dictionary of transformation cache
        """
        if not os.path.exists(self.transformation_cache_file):
            return {}
        
        try:
            with open(self.transformation_cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warn(f"Error loading transformation cache: {e}")
            return {}
    
    def _save_transformation_cache(self):
        """
        Save the transformation cache to disk.
        """
        try:
            with open(self.transformation_cache_file, 'w') as f:
                json.dump(self.transformation_cache, f)
        except Exception as e:
            logger.warn(f"Error saving transformation cache: {e}")
    
    def _check_transformation_cache(self, original_locator):
        """
        Check if we've seen a similar locator pattern before.
        
        :param original_locator: The original locator that failed
        :return: Cached transformed locator if available, otherwise None
        """
        # Direct match
        if original_locator in self.transformation_cache:
            return self.transformation_cache[original_locator]
        
        # Pattern match for similar locators
        for cached_locator, transformed_locator in self.transformation_cache.items():
            # Check if the original locator has the same structure pattern
            if self._similar_locator_pattern(original_locator, cached_locator):
                logger.info(f"Found similar locator pattern: {cached_locator}")
                return self._adapt_transformation(original_locator, cached_locator, transformed_locator)
                
        return None
    
    def _similar_locator_pattern(self, locator1, locator2):
        """
        Check if two locators have a similar pattern.
        
        :param locator1: First locator
        :param locator2: Second locator
        :return: True if locators have a similar pattern
        """
        # Simple check for now: same prefix and similar structure
        if locator1.startswith('css=') and locator2.startswith('css='):
            # Compare structure (e.g., number of classes, IDs, attributes)
            pattern1 = re.sub(r'[a-zA-Z0-9_-]+', 'X', locator1)
            pattern2 = re.sub(r'[a-zA-Z0-9_-]+', 'X', locator2)
            return pattern1 == pattern2
        elif locator1.startswith('xpath=') and locator2.startswith('xpath='):
            # Compare structure of XPath expressions
            pattern1 = re.sub(r'@[a-zA-Z0-9_-]+=[\'""][^\'"]*[\'"]', '@X=Y', locator1)
            pattern2 = re.sub(r'@[a-zA-Z0-9_-]+=[\'""][^\'"]*[\'"]', '@X=Y', locator2)
            return pattern1 == pattern2
            
        return False
    
    def _adapt_transformation(self, original_locator, cached_locator, transformed_locator):
        """
        Adapt a cached transformation to a new original locator.
        
        :param original_locator: The new original locator
        :param cached_locator: The cached original locator
        :param transformed_locator: The cached transformed locator
        :return: Adapted transformation for the new original locator
        """
        # For now, just return the transformed locator
        # Could be enhanced to adapt the transformation based on differences
        return transformed_locator
    
    def _store_transformation(self, original_locator, transformed_locator):
        """
        Store a successful transformation in the cache.
        
        :param original_locator: The original locator that failed
        :param transformed_locator: The transformed locator that worked
        """
        # Only store if the locators are different
        if original_locator != transformed_locator:
            self.transformation_cache[original_locator] = transformed_locator
            self._save_transformation_cache()
            logger.info(f"Stored transformation: {original_locator} → {transformed_locator}") 