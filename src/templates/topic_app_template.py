from typing import Dict, Any, Optional, List
from .project_templates import ProjectTemplate, ProjectType, Framework

class TopicAppTemplate(ProjectTemplate):
    """Template for generating apps of any topic."""
    
    def __init__(self, topic: str, framework: Framework = Framework.FLASK):
        super().__init__(f"{topic.title()} App", ProjectType.WEB_APP, framework)
        self.topic = topic
        self._initialize_template()
    
    def _initialize_template(self):
        """Initialize template files and dependencies based on topic."""
        if self.framework == Framework.FLASK:
            self.dependencies = [
                "flask>=2.0.0",
                "flask-sqlalchemy>=3.0.0",
                "flask-login>=0.6.0",
                "flask-wtf>=1.0.0",
                "python-dotenv>=1.0.0",
                "sqlalchemy>=2.0.0",
                "werkzeug>=2.0.0",
                "jinja2>=3.0.0",
                "requests>=2.0.0",
            ]
            
            self.files = {
                "__init__.py": "",
                "config.py": self._get_config_code(),
                "models.py": self._get_models_code(),
                "routes.py": self._get_routes_code(),
                "forms.py": self._get_forms_code(),
                "utils.py": self._get_utils_code(),
                "templates/base.html": self._get_base_template(),
                "templates/index.html": self._get_index_template(),
                "static/css/style.css": self._get_css_code(),
                "static/js/main.js": self._get_js_code(),
            }
            
            self.config_files = {
                ".env.example": self._get_env_example(),
                "config.yaml": self._get_config_yaml(),
            }
    
    def _get_config_code(self) -> str:
        """Generate config.py code."""
        return f'''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{self.topic.lower()}.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''

    def _get_models_code(self) -> str:
        """Generate models.py code."""
        return f'''from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Add topic-specific models here
'''

    def _get_routes_code(self) -> str:
        """Generate routes.py code."""
        return f'''from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import db
from .forms import SearchForm

bp = Blueprint('{self.topic.lower()}', __name__)

@bp.route('/')
def index():
    """Home page."""
    return render_template('index.html', title='{self.topic.title()} App')

@bp.route('/search')
def search():
    """Search functionality."""
    form = SearchForm()
    if form.validate_on_submit():
        # Add search logic here
        pass
    return render_template('search.html', form=form)

# Add more routes based on topic
'''

    def _get_forms_code(self) -> str:
        """Generate forms.py code."""
        return '''from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """Search form."""
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
'''

    def _get_utils_code(self) -> str:
        """Generate utils.py code."""
        return '''from typing import Any, Dict, List, Optional

def format_data(data: Any) -> Dict[str, Any]:
    """Format data for display."""
    if isinstance(data, dict):
        return {k: format_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [format_data(item) for item in data]
    return str(data)

def validate_input(data: str) -> bool:
    """Validate user input."""
    return bool(data and data.strip())
'''

    def _get_base_template(self) -> str:
        """Generate base.html template."""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ title or '{self.topic.title()} App' }}}}</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
</head>
<body>
    <header>
        <nav>
            <div class="nav-wrapper">
                <a href="{{{{ url_for('index') }}}}" class="brand-logo">{self.topic.title()}</a>
                <ul class="nav-links">
                    <li><a href="{{{{ url_for('index') }}}}">Home</a></li>
                    <li><a href="{{{{ url_for('search') }}}}">Search</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main>
        {{% block content %}}{{% endblock %}}
    </main>

    <footer>
        <p>&copy; 2025 {self.topic.title()} App. All rights reserved.</p>
    </footer>

    <script src="{{{{ url_for('static', filename='js/main.js') }}}}"></script>
</body>
</html>
'''

    def _get_index_template(self) -> str:
        """Generate index.html template."""
        return f'''{{% extends "base.html" %}}

{{% block content %}}
<div class="container">
    <h1>Welcome to {self.topic.title()}</h1>
    <p>Discover and explore everything about {self.topic.lower()}!</p>
    
    <div class="search-section">
        <form method="GET" action="{{{{ url_for('search') }}}}">
            {{{{ form.hidden_tag() }}}}
            <div class="form-group">
                {{{{ form.query.label }}}}
                {{{{ form.query(class="form-control") }}}}
            </div>
            {{{{ form.submit(class="btn btn-primary") }}}}
        </form>
    </div>
</div>
{{% endblock %}}
'''

    def _get_css_code(self) -> str:
        """Generate style.css code."""
        return '''/* Modern CSS with variables */
:root {
    --primary-color: #2196F3;
    --secondary-color: #FFC107;
    --text-color: #333;
    --background-color: #fff;
    --font-family: 'Segoe UI', system-ui, sans-serif;
}

/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-family);
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
}

/* Navigation */
.nav-wrapper {
    background-color: var(--primary-color);
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand-logo {
    color: white;
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 1rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.nav-links a:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* Forms */
.form-group {
    margin-bottom: 1rem;
}

.form-control {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: #1976D2;
}

/* Footer */
footer {
    text-align: center;
    padding: 1rem;
    background-color: #f5f5f5;
    margin-top: 2rem;
}
'''

    def _get_js_code(self) -> str:
        """Generate main.js code."""
        return '''// Add interactive features
document.addEventListener('DOMContentLoaded', () => {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const required = form.querySelectorAll('[required]');
            required.forEach(field => {
                if (!field.value) {
                    e.preventDefault();
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
        });
    });

    // Dynamic search suggestions
    const searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(async (e) => {
            const query = e.target.value;
            if (query.length >= 2) {
                try {
                    const response = await fetch(`/api/search/suggestions?q=${encodeURIComponent(query)}`);
                    const suggestions = await response.json();
                    updateSuggestions(suggestions);
                } catch (error) {
                    console.error('Error fetching suggestions:', error);
                }
            }
        }, 300));
    }
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function updateSuggestions(suggestions) {
    const container = document.querySelector('.search-suggestions');
    if (!container) return;
    
    container.innerHTML = suggestions
        .map(s => `<div class="suggestion">${s}</div>`)
        .join('');
}
'''

    def _get_env_example(self) -> str:
        """Generate .env.example file."""
        return '''# Application settings
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db

# API keys (if needed)
API_KEY=your-api-key-here
'''

    def _get_config_yaml(self) -> str:
        """Generate config.yaml file."""
        return f'''# {self.topic.title()} App Configuration

app:
  name: "{self.topic.title()} App"
  description: "A web application for {self.topic.lower()}"
  version: "1.0.0"

server:
  host: "0.0.0.0"
  port: 5000
  debug: false

database:
  type: "sqlite"
  name: "{self.topic.lower()}.db"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/app.log"

security:
  password_min_length: 8
  password_max_length: 128
  require_special_chars: true
  require_numbers: true
'''
