# src/web_browser.py
import os
import requests
from openai import OpenAI
import pdfplumber
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import html2text
from fake_useragent import UserAgent
import time
from datetime import datetime
from karhu.Errors import Errors
from termcolor import colored
import httpx

class WebBrowser:
    """Handles web browsing and searching"""
    def __init__(self):
        self.user_agent = UserAgent()
        self.session = requests.Session()
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = True
        self.h2t.ignore_images = True
        self.client = httpx.Client(timeout=10)
        
    def get_headers(self):
        return {
            'User-Agent': self.user_agent.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
    
    def browse_url(self, url):
        try:
            if not urlparse(url).scheme:
                url = 'https://' + url
            
            # Add logging to see what URL is being requested
            print(f"Attempting to browse: {url}")
                
            response = self.session.get(url, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
    
            # Log response details for debugging
            print(f"Successfully fetched: {url}, Status Code: {response.status_code}")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted tags
            for tag in soup(['script', 'style', 'nav', 'footer', 'iframe']):
                tag.decompose()
                
            # Convert HTML to text
            text = self.h2t.handle(str(soup))
            # print(f"header : {text.strip()}")  # Log the first 100 characters of the text
            return text.strip()
            
        except httpx.HTTPStatusError as http_err:
            return f"HTTP error occurred: {http_err.response.status_code} {http_err.response.text}"
        except httpx.RequestError as req_err:
            return f"Request error occurred: {req_err}"
        except Exception as e:
            return f"Unexpected error occurred: {str(e)}"
    
    def search_duckduckgo(self, query, num_results=5):
        try:
            url = "https://html.duckduckgo.com/html/"
            params = {'q': query}
            
            # Add logging to see what query is being performed
            print(f"Searching DuckDuckGo for query: {query}")
            
            response = self.session.get(
                url, 
                params=params, 
                headers=self.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            # Log response details for debugging
            print(f"Search request successful, Status Code: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Parse the search results
            for result in soup.select('.result'):
                title_elem = result.select_one('.result__title')
                link_elem = result.select_one('.result__url')
                snippet_elem = result.select_one('.result__snippet')
                
                if title_elem and link_elem:
                    results.append({
                        'title': title_elem.get_text().strip(),
                        'url': link_elem.get_text().strip(),
                        'snippet': snippet_elem.get_text().strip() if snippet_elem else ''
                    })
                    
                if len(results) >= num_results:
                    break
                    
            # Return the results
            return results
            
        except requests.exceptions.RequestException as e:
            # Specific handling of request exceptions
            return f"Error performing search: {str(e)}"
        except Exception as e:
            # Catch any other errors
            return f"Unexpected error: {str(e)}"
