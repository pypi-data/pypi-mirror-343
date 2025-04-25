#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
from robot.api import logger

class AIProcessor:
    """
    Handles AI processing functions for DOM element locator generation.
    """
    
    def __init__(self, api_key=None, api_url="https://api.openai.com/v1/chat/completions", model="gpt-4o"):
        """
        Initialize the AI processor.
        
        :param api_key: OpenAI API key
        :param api_url: OpenAI API endpoint URL
        :param model: OpenAI model to use
        """
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        
    def generate_locator(self, html, element_description):
        """
        Generate a locator for an element based on its description.
        
        :param html: HTML content of the page
        :param element_description: Natural language description of the element
        :return: AI-generated locator
        """
        if not self.api_key:
            raise Exception("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            
        # Process the HTML to reduce its size
        processed_html = self._preprocess_html(html)
        
        if not processed_html:
            raise ValueError("No HTML content to analyze after preprocessing")
            
        # Call OpenAI API
        ai_locator = self._call_openai_api(processed_html, element_description)
        
        return ai_locator
        
    def derive_contextual_locator(self, html, description):
        """
        Derive a basic locator from context when API is unavailable.
        This is a fallback method used when the API call fails.
        
        :param html: HTML content
        :param description: Element description
        :return: A context-derived locator
        """
        try:
            description = description.lower()

            # This method handles common patterns for the demo
            if "username" in description or "user" in description:
                return "css=input[type='text']"
            elif "password" in description:
                return "css=input[type='password']"
            elif "login" in description or "submit" in description or "button" in description:
                return "css=input[type='submit'], button[type='submit'], button"
            elif "product" in description or "inventory" in description:
                return "css=.product_label, .inventory_item"
            else:
                # Default case - look for input or common containers
                return "css=input"
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

            # Remove hidden elements
            html = re.sub(r'<[^>]*?style\s*=\s*["\'][^"\']*?(display:\s*none|visibility:\s*hidden)[^"\']*?["\'][^>]*>.*?</[^>]*>', '', html, flags=re.DOTALL)

            # Focus on body content if possible
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
            if body_match:
                html = body_match.group(1)

            # Truncate if still too long
            if len(html) > max_length:
                html = html[:max_length]

            return html
        except Exception as e:
            logger.warn(f"HTML preprocessing failed: {e}. Using truncated HTML.")
            return html[:max_length] if html and len(html) > max_length else ""
            
    def _call_openai_api(self, html, description):
        """
        Call the OpenAI API to get a locator based on the description.

        :param html: Preprocessed HTML content
        :param description: Natural language description of the element
        :return: AI-generated locator
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        messages = [
            {"role": "system", "content": "You are a web automation expert that helps find CSS or XPath selectors for web elements."},
            {"role": "user", "content": f"""Given the following HTML, provide a CSS selector or XPath that precisely identifies the element described as: "{description}". 
            
Return ONLY the selector as a raw string, without any explanation, quotes, or formatting.

HTML:
{html}
"""}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,  # Lower temperature for more deterministic results
            "max_tokens": 250,
        }

        logger.debug(f"Calling OpenAI API with model: {self.model}")

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