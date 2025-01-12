from enum import Enum
from typing import Dict, Any, Optional, List

class ProjectType(Enum):
    WEB_APP = "web_app"
    CLI_TOOL = "cli_tool"
    DESKTOP_APP = "desktop_app"
    GAME = "game"
    DATA_SCIENCE = "data_science"
    AI_ASSISTANT = "ai_assistant"
    TOPIC_APP = "topic_app"
    GENERAL = "general"

class Framework(Enum):
    FLASK = "flask"
    DJANGO = "django"
    FASTAPI = "fastapi"
    STREAMLIT = "streamlit"
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    PYGAME = "pygame"
    TKINTER = "tkinter"
    QT = "qt"
    NONE = "none"

class ProjectTemplate:
    """Base class for all project templates."""
    
    def __init__(self, name: str, project_type: ProjectType, framework: Optional[Framework] = None):
        self.name = name
        self.project_type = project_type
        self.framework = framework
        self.files: Dict[str, str] = {}
        self.dependencies: List[str] = []
        self.config_files: Dict[str, str] = {}
    
    def get_structure(self) -> Dict[str, Any]:
        """Get project structure."""
        return {
            "src": {
                "main.py": "",
                "utils": {},
                "tests": {}
            },
            "docs": {},
            "config": {}
        }
    
    def get_files(self) -> Dict[str, str]:
        """Get template files."""
        return self.files
    
    def get_dependencies(self) -> List[str]:
        """Get project dependencies."""
        return self.dependencies
    
    def get_config_files(self) -> Dict[str, str]:
        """Get configuration files."""
        return self.config_files
    
    def get_test_framework(self) -> str:
        """Get test framework."""
        return "pytest"

class WebScraperTemplate(ProjectTemplate):
    """Template for web scraper projects."""
    
    def __init__(self):
        super().__init__("Web Scraper", ProjectType.GENERAL)
        self._initialize_template()
    
    def _initialize_template(self):
        """Initialize template files and dependencies."""
        self.files = {
            "scraper.py": '''from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Any
import json
import os

class WebScraper:
    """Web scraper using Beautiful Soup."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def scrape_page(self, url: str) -> BeautifulSoup:
        """Scrape a single page and return the parsed HTML."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def extract_data(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, Any]:
        """Extract data from the page using CSS selectors."""
        data = {}
        for key, selector in selectors.items():
            elements = soup.select(selector)
            data[key] = [elem.text.strip() for elem in elements]
        return data
    
    def save_data(self, data: List[Dict[str, Any]], filename: str):
        """Save scraped data to a JSON file."""
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
''',
            "main.py": '''from flask import Flask, render_template, request, jsonify
from scraper import WebScraper
import os

app = Flask(__name__)
scraper = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    selectors = data.get('selectors', {})
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    global scraper
    if scraper is None:
        scraper = WebScraper(url)
    
    # Scrape the page
    soup = scraper.scrape_page(url)
    if soup is None:
        return jsonify({'error': 'Failed to scrape page'}), 500
    
    # Extract data
    extracted_data = scraper.extract_data(soup, selectors)
    
    # Save data
    scraper.save_data([extracted_data], 'scraped_data.json')
    
    return jsonify(extracted_data)

@app.route('/results')
def results():
    filepath = os.path.join('data', 'scraped_data.json')
    if not os.path.exists(filepath):
        return jsonify([])
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
'''
        }
        
        self.dependencies = [
            "beautifulsoup4>=4.9.3",
            "requests>=2.25.1",
            "flask>=2.0.1"
        ]
        
        self.config_files = {
            "requirements.txt": "\n".join(self.dependencies),
            "README.md": '''# Web Scraper

A web scraping application built with Beautiful Soup and Flask.

## Features

- Web page scraping using Beautiful Soup
- Data extraction using CSS selectors
- JSON data storage
- Web interface for easy interaction

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter the URL you want to scrape
2. Specify CSS selectors in JSON format
3. Click "Start Scraping"
4. View the results in JSON format
'''
        }

def get_template(project_type: ProjectType, framework: Optional[Framework] = None, topic: Optional[str] = None) -> ProjectTemplate:
    """Get project template based on type and framework.
    
    Args:
        project_type: Type of project to create
        framework: Framework to use (optional)
        topic: Topic for topic-based apps (optional)
    """
    if project_type == ProjectType.TOPIC_APP:
        from .topic_app_template import TopicAppTemplate
        if not topic:
            raise ValueError("Topic must be provided for topic-based apps")
        return TopicAppTemplate(topic, framework or Framework.FLASK)
        
    if project_type == ProjectType.WEB_APP:
        if framework == Framework.FLASK:
            return FlaskTemplate()
        elif framework == Framework.DJANGO:
            return DjangoTemplate()
        elif framework == Framework.FASTAPI:
            return FastAPITemplate()
        return FlaskTemplate()
    
    elif project_type == ProjectType.CLI_TOOL:
        return CLITemplate()
    
    elif project_type == ProjectType.DESKTOP_APP:
        if framework == Framework.TKINTER:
            return TkinterTemplate()
        elif framework == Framework.QT:
            return QtTemplate()
        return TkinterTemplate()
    
    elif project_type == ProjectType.GAME:
        return GameTemplate()
    
    elif project_type == ProjectType.DATA_SCIENCE:
        return DataScienceTemplate()
    
    elif project_type == ProjectType.AI_ASSISTANT:
        return AIAssistantTemplate()
    
    else:
        return GeneralTemplate()
