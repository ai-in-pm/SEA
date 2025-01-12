from typing import Dict, Any, List
from ..llm import LLMManager
from ..templates.project_templates import ProjectTemplate

class CodeGenerator:
    """Generates code based on project specifications."""
    
    def __init__(self, llm: LLMManager):
        self.llm = llm
    
    def generate_code(self, specs: Dict[str, Any], template: ProjectTemplate) -> Dict[str, str]:
        """Generate code files based on project specifications."""
        code = {}
        
        # Get template files
        template_files = template.get_files()
        for filepath, content in template_files.items():
            code[filepath] = content
        
        # Generate additional code based on specs
        if "web scraper" in specs.get("description", "").lower():
            code.update(self._generate_web_scraper_code(specs))
        
        return code
    
    def generate_tests(self, code: Dict[str, str], template: ProjectTemplate) -> Dict[str, str]:
        """Generate test files for the code."""
        tests = {}
        
        # Generate test files for each code file
        for filepath, content in code.items():
            test_name = f"test_{filepath}"
            try:
                task = f"Generate tests for {filepath}"
                component = "tests"
                tests[test_name] = self.llm.generate(
                    task=task,
                    component=component
                ) or self._generate_test_file(filepath, content)
            except Exception as e:
                tests[test_name] = self._generate_test_file(filepath, content)
        
        return tests
    
    def generate_documentation(self, code: Dict[str, str], tests: Dict[str, str], template: ProjectTemplate) -> Dict[str, str]:
        """Generate documentation for the project."""
        docs = {}
        
        # Generate README.md
        try:
            task = "Generate project documentation including setup and usage instructions"
            component = "documentation"
            readme_prompt = "Generate README.md for a project with the following files:\n\n"
            for filepath, content in code.items():
                readme_prompt += f"File: {filepath}\n{content}\n\n"
            docs["README.md"] = self.llm.generate(
                task=readme_prompt,
                component=component
            ) or self._generate_readme(code, tests)
        except Exception as e:
            docs["README.md"] = self._generate_readme(code, tests)
        
        # Generate CONTRIBUTING.md
        try:
            task = "Generate contributing guide for the project"
            component = "contributing"
            docs["CONTRIBUTING.md"] = self.llm.generate(
                task=task,
                component=component
            ) or self._generate_contributing_guide()
        except Exception as e:
            docs["CONTRIBUTING.md"] = self._generate_contributing_guide()
        
        # Generate API.md
        try:
            task = "Generate API documentation"
            component = "api_docs"
            api_prompt = "Generate API documentation for the following files:\n\n"
            for filepath, content in code.items():
                api_prompt += f"File: {filepath}\n{content}\n\n"
            docs["API.md"] = self.llm.generate(
                task=api_prompt,
                component=component
            ) or self._generate_api_documentation(code)
        except Exception as e:
            docs["API.md"] = self._generate_api_documentation(code)
        
        return docs
    
    def _generate_web_scraper_code(self, specs: Dict[str, Any]) -> Dict[str, str]:
        """Generate code for a web scraper project."""
        code = {}
        
        # Generate scraper.py
        try:
            task = "Generate a web scraper class using Beautiful Soup with methods for scraping pages, extracting data, and saving to JSON"
            component = "scraper"
            code["scraper.py"] = self.llm.generate(
                task=task,
                component=component
            ) or '''from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Any
import json
import os

class WebScraper:
    """A web scraper class for extracting data from web pages."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url
        self.session = requests.Session()
    
    def scrape_page(self, url: str) -> BeautifulSoup:
        """Scrape a web page and return its BeautifulSoup object."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def extract_data(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, Any]:
        """Extract data from a BeautifulSoup object using CSS selectors."""
        data = {}
        if not soup:
            return data
        
        for key, selector in selectors.items():
            elements = soup.select(selector)
            data[key] = [elem.text.strip() for elem in elements]
        
        return data
    
    def save_to_json(self, data: Dict[str, Any], filename: str) -> None:
        """Save extracted data to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")
'''
        except Exception as e:
            code["scraper.py"] = '''from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Any
import json
import os

class WebScraper:
    """A web scraper class for extracting data from web pages."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url
        self.session = requests.Session()
    
    def scrape_page(self, url: str) -> BeautifulSoup:
        """Scrape a web page and return its BeautifulSoup object."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def extract_data(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, Any]:
        """Extract data from a BeautifulSoup object using CSS selectors."""
        data = {}
        if not soup:
            return data
        
        for key, selector in selectors.items():
            elements = soup.select(selector)
            data[key] = [elem.text.strip() for elem in elements]
        
        return data
    
    def save_to_json(self, data: Dict[str, Any], filename: str) -> None:
        """Save extracted data to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")
'''
        
        # Generate routes.py
        try:
            task = "Generate Flask routes for a web scraper with endpoints for the main page and scraping functionality"
            component = "routes"
            code["routes.py"] = self.llm.generate(
                task=task,
                component=component
            ) or '''from flask import Blueprint, render_template, request, jsonify
from .scraper import WebScraper
import json
import os

bp = Blueprint('scraper', __name__)
scraper = WebScraper()

@bp.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@bp.route('/scrape', methods=['POST'])
def scrape():
    """Handle scraping requests."""
    data = request.get_json()
    url = data.get('url')
    selectors = data.get('selectors', {})
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Scrape the page
    soup = scraper.scrape_page(url)
    if not soup:
        return jsonify({'error': 'Failed to scrape page'}), 500
    
    # Extract data
    result = scraper.extract_data(soup, selectors)
    
    # Save to file
    output_file = os.path.join('data', 'scraped_data.json')
    os.makedirs('data', exist_ok=True)
    scraper.save_to_json(result, output_file)
    
    return jsonify(result)

@bp.route('/load', methods=['GET'])
def load():
    """Load previously scraped data."""
    try:
        with open(os.path.join('data', 'scraped_data.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''
        except Exception as e:
            code["routes.py"] = '''from flask import Blueprint, render_template, request, jsonify
from .scraper import WebScraper
import json
import os

bp = Blueprint('scraper', __name__)
scraper = WebScraper()

@bp.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@bp.route('/scrape', methods=['POST'])
def scrape():
    """Handle scraping requests."""
    data = request.get_json()
    url = data.get('url')
    selectors = data.get('selectors', {})
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Scrape the page
    soup = scraper.scrape_page(url)
    if not soup:
        return jsonify({'error': 'Failed to scrape page'}), 500
    
    # Extract data
    result = scraper.extract_data(soup, selectors)
    
    # Save to file
    output_file = os.path.join('data', 'scraped_data.json')
    os.makedirs('data', exist_ok=True)
    scraper.save_to_json(result, output_file)
    
    return jsonify(result)

@bp.route('/load', methods=['GET'])
def load():
    """Load previously scraped data."""
    try:
        with open(os.path.join('data', 'scraped_data.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''
        
        return code
    
    def _generate_test_file(self, filepath: str, content: str) -> str:
        """Generate a test file for the given code file."""
        return f'''import unittest
from {filepath.replace(".py", "")} import *

class Test{filepath.replace(".py", "").title()}(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_basic_functionality(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
'''
    
    def _generate_readme(self, code: Dict[str, str], tests: Dict[str, str]) -> str:
        """Generate README.md content."""
        return '''# Web Scraper Project

A web scraping application built with Beautiful Soup and Flask.

## Features

- Web page scraping using Beautiful Soup
- Data extraction using CSS selectors
- JSON data storage
- RESTful API endpoints
- Web interface for scraping

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python src/main.py`

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Enter the URL to scrape and CSS selectors
3. Click "Scrape" to start scraping
4. View the extracted data in the results section

## API Endpoints

- `GET /`: Web interface
- `POST /scrape`: Scrape a URL with specified selectors

## Contributing

See CONTRIBUTING.md for guidelines.

## License

MIT License
'''
    
    def _generate_contributing_guide(self) -> str:
        """Generate CONTRIBUTING.md content."""
        return '''# Contributing Guide

Thank you for considering contributing to this project!

## Getting Started

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `python -m unittest discover tests`
5. Submit a pull request

## Code Style

- Follow PEP 8 guidelines
- Write docstrings for functions and classes
- Add type hints where possible
- Write unit tests for new features

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update README.md if needed
5. Submit pull request with clear description

## Questions?

Feel free to open an issue for questions or suggestions.
'''
    
    def _generate_api_documentation(self, code: Dict[str, str]) -> str:
        """Generate API.md content."""
        return '''# API Documentation

## Endpoints

### GET /

Web interface for the scraper.

### POST /scrape

Scrape a URL with specified selectors.

#### Request Body

```json
{
    "url": "https://example.com",
    "selectors": {
        "title": "h1",
        "content": "p.content"
    }
}
```

#### Response

```json
{
    "title": ["Example Title"],
    "content": ["Example content paragraph"]
}
```

## Error Handling

- 400: Bad Request (missing URL)
- 500: Server Error (scraping failed)
'''
