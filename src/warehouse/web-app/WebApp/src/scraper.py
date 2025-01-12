from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Any
import json
import os

class WebScraper:
    """Web scraper using Beautiful Soup."""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape(self, url: str) -> str:
        """Scrape a webpage and return formatted HTML content."""
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content
            content = []
            
            # Get title
            if soup.title:
                content.append(f'<h2>Page Title:</h2><p>{soup.title.string}</p>')
            
            # Get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                content.append(f'<h2>Meta Description:</h2><p>{meta_desc["content"]}</p>')
            
            # Get headings
            headings = soup.find_all(['h1', 'h2', 'h3'])
            if headings:
                content.append('<h2>Main Headings:</h2><ul>')
                for heading in headings[:10]:  # Limit to first 10 headings
                    content.append(f'<li>{heading.get_text().strip()}</li>')
                content.append('</ul>')
            
            # Get links
            links = soup.find_all('a', href=True)
            if links:
                content.append('<h2>Links Found:</h2><ul>')
                seen_links = set()
                for link in links:
                    href = link['href']
                    text = link.get_text().strip()
                    if href and text and href not in seen_links:
                        seen_links.add(href)
                        if len(seen_links) > 10:  # Limit to 10 unique links
                            break
                        content.append(f'<li><strong>{text}</strong>: {href}</li>')
                content.append('</ul>')
            
            # Get images
            images = soup.find_all('img', alt=True)
            if images:
                content.append('<h2>Images:</h2><ul>')
                for img in images[:5]:  # Limit to first 5 images
                    content.append(f'<li>Alt text: {img["alt"]}</li>')
                content.append('</ul>')
            
            return '\n'.join(content)
            
        except requests.RequestException as e:
            raise Exception(f"Error scraping {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing page: {str(e)}")
