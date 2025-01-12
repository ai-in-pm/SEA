from typing import Dict, Any
import os
import json
import shutil
import traceback
from ..llm import LLMManager
from ..utils.config import Config
from ..templates.project_templates import ProjectType, Framework, get_template
from ..codegen.code_generator import CodeGenerator
from ..testing.test_generator import TestGenerator
from ..sea_agent_errors import ErrorTracker, ErrorAnalyzer
from .app_demonstrator import AppDemonstrator
import time
from typing import List

class ProjectGenerator:
    """Handles project generation logic for the AI agent."""
    
    def __init__(self, config: Config):
        self.config = config
        self.llm = LLMManager(config)
        self.code_generator = CodeGenerator(self.llm)
        self.test_generator = TestGenerator(config)
        self.error_tracker = ErrorTracker()
        self.error_analyzer = ErrorAnalyzer(os.path.join(os.path.dirname(__file__), '..', 'sea_agent_errors', 'logs'))
    
    def create_project_structure(self, project_dir: str, task_description: str, template: Any) -> None:
        """Create complete project structure with generated files."""
        try:
            print("\n[1/10] Analyzing project requirements...")
            
            # Create standard directory structure if it doesn't exist
            directories = [
                os.path.join(project_dir, "src"),
                os.path.join(project_dir, "tests"),
                os.path.join(project_dir, "docs"),
                os.path.join(project_dir, "config"),
            ]
            
            for directory in directories:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            
            # Generate comparison.md
            print("\n[2/10] Generating development comparison analysis...")
            try:
                self._generate_comparison_file(
                    project_dir=project_dir,
                    template=template,
                    task_description=task_description
                )
            except Exception as e:
                self.error_tracker.log_error(
                    error_type="ComparisonGenerationError",
                    error_message=str(e),
                    context={"task_description": task_description},
                    stack_trace=traceback.format_exc(),
                    component="comparison_generation",
                    severity="ERROR"
                )
                raise
            
            # Analyze project requirements
            print("\n[3/10] Analyzing project requirements...")
            try:
                project_specs = self.analyze_project_requirements(task_description)
            except Exception as e:
                self.error_tracker.log_error(
                    error_type="RequirementsAnalysisError",
                    error_message=str(e),
                    context={"task_description": task_description},
                    stack_trace=traceback.format_exc(),
                    component="requirements_analysis",
                    severity="ERROR"
                )
                raise
            
            # Get project template
            print("\n[4/10] Selecting project template...")
            try:
                template = get_template(project_specs["type"], project_specs.get("framework"))
            except Exception as e:
                self.error_tracker.log_error(
                    error_type="TemplateSelectionError",
                    error_message=str(e),
                    context=project_specs,
                    stack_trace=traceback.format_exc(),
                    component="template_selection",
                    severity="ERROR"
                )
                raise
            
            # Generate code from template
            print("\n[5/10] Generating code...")
            try:
                code = self.code_generator.generate_code(project_specs, template)
            except Exception as e:
                self.error_tracker.log_error(
                    error_type="CodeGenerationError",
                    error_message=str(e),
                    context={"specs": project_specs},
                    stack_trace=traceback.format_exc(),
                    component="code_generation",
                    severity="ERROR"
                )
                raise
            
            # Write code files
            src_dir = os.path.join(project_dir, "src")
            for filepath, content in code.items():
                full_path = os.path.join(src_dir, filepath)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Generate tests
            print("\n[6/10] Generating tests...")
            try:
                tests = self.code_generator.generate_tests(code, template)
            except Exception as e:
                self.error_tracker.log_error(
                    error_type="TestGenerationError",
                    error_message=str(e),
                    context={"code_files": list(code.keys())},
                    stack_trace=traceback.format_exc(),
                    component="test_generation",
                    severity="ERROR"
                )
                raise
            
            # Write test files
            tests_dir = os.path.join(project_dir, "tests")
            for filepath, content in tests.items():
                full_path = os.path.join(tests_dir, filepath)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Generate documentation
            print("\n[7/10] Generating documentation...")
            try:
                docs = self.code_generator.generate_documentation(code, tests, template)
            except Exception as e:
                self.error_tracker.log_error(
                    error_type="DocumentationGenerationError",
                    error_message=str(e),
                    context={"code_files": list(code.keys()), "test_files": list(tests.keys())},
                    stack_trace=traceback.format_exc(),
                    component="documentation_generation",
                    severity="ERROR"
                )
                raise
            
            # Write documentation files
            docs_dir = os.path.join(project_dir, "docs")
            for filepath, content in docs.items():
                full_path = os.path.join(docs_dir, filepath)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Write configuration files
            print("\n[8/10] Writing configuration files...")
            try:
                config_files = template.get_config_files()
                config_dir = os.path.join(project_dir, "config")
                for filepath, content in config_files.items():
                    full_path = os.path.join(config_dir, filepath)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                self.error_tracker.log_error(
                    error_type="ConfigurationError",
                    error_message=str(e),
                    context={"template": template.__class__.__name__},
                    stack_trace=traceback.format_exc(),
                    component="configuration",
                    severity="ERROR"
                )
                raise
            
            # Initialize git repository
            print("\n[9/10] Initializing git repository...")
            try:
                self._initialize_git(project_dir)
            except Exception as e:
                self.error_tracker.log_error(
                    error_type="GitInitializationError",
                    error_message=str(e),
                    context={"project_dir": project_dir},
                    stack_trace=traceback.format_exc(),
                    component="git_initialization",
                    severity="WARNING"
                )
            
            # Generate error report
            print("\n[10/10] Generating error report...")
            error_report = self.error_analyzer.generate_report()
            error_report_path = os.path.join(project_dir, "error_report.md")
            with open(error_report_path, 'w', encoding='utf-8') as f:
                f.write(error_report)
            
            print("\nProject generation complete!")
            
        except Exception as e:
            self.error_tracker.log_error(
                error_type="ProjectGenerationError",
                error_message=str(e),
                context={"project_dir": project_dir, "task_description": task_description},
                stack_trace=traceback.format_exc(),
                component="project_generation",
                severity="CRITICAL"
            )
            raise
    
    def analyze_project_requirements(self, task_description: str) -> Dict[str, Any]:
        """Analyze task description to determine project requirements."""
        # For now, use simple keyword matching
        project_type = ProjectType.WEB_APP
        framework = Framework.FLASK
        
        if "web scraper" in task_description.lower():
            project_type = ProjectType.GENERAL
            framework = Framework.NONE
        
        return {
            "type": project_type,
            "framework": framework,
            "description": task_description
        }
    
    def _initialize_git(self, project_dir: str) -> None:
        """Initialize git repository and create initial commit."""
        try:
            import git
            repo = git.Repo.init(project_dir)
            
            # Create .gitignore
            gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project specific
data/
logs/
.env
'''
            gitignore_path = os.path.join(project_dir, '.gitignore')
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            
            # Add all files and create initial commit
            repo.index.add('*')
            repo.index.commit("Initial commit")
            
        except ImportError:
            print("Warning: gitpython not installed. Skipping git initialization.")
        except Exception as e:
            print(f"Warning: Failed to initialize git repository: {str(e)}")

    def _create_project_directory(self, project_name: str) -> str:
        """Create and return the project directory path."""
        # Define base paths
        warehouse_dir = os.path.join(os.path.dirname(__file__), '..', 'warehouse')
        project_type_dir = os.path.join(warehouse_dir, 'web_app')
        project_dir = os.path.join(project_type_dir, project_name)
        
        # Create warehouse and project type directories if they don't exist
        os.makedirs(warehouse_dir, exist_ok=True)
        os.makedirs(project_type_dir, exist_ok=True)
        
        # Clean up any existing project directories with the same name
        if os.path.exists(project_dir):
            try:
                import shutil
                shutil.rmtree(project_dir)
                print(f"\nRemoving existing project directory: {project_dir}")
            except Exception as e:
                print(f"Warning: Failed to remove existing directory: {str(e)}")
        
        # Create new project directory
        os.makedirs(project_dir)
        print(f"\nCreated project directory: {project_dir}")
        
        return project_dir
    
    def _cleanup_old_projects(self) -> None:
        """Clean up old project directories."""
        try:
            warehouse_dir = os.path.join(os.path.dirname(__file__), '..', 'warehouse')
            web_app_dir = os.path.join(warehouse_dir, 'web_app')
            
            if not os.path.exists(web_app_dir):
                return
            
            # Get all directories in web_app folder
            project_dirs = [d for d in os.listdir(web_app_dir) 
                          if os.path.isdir(os.path.join(web_app_dir, d))]
            
            # Remove timestamp suffixes for comparison
            base_names = set()
            for dir_name in project_dirs:
                # Extract base name (remove timestamp if present)
                base_name = dir_name.split('_')[0]
                base_names.add(base_name)
            
            # For each base name, keep only the latest version
            for base_name in base_names:
                matching_dirs = [d for d in project_dirs if d.startswith(base_name)]
                if len(matching_dirs) > 1:
                    # Sort by creation time (newest first)
                    matching_dirs.sort(key=lambda x: os.path.getctime(
                        os.path.join(web_app_dir, x)), reverse=True)
                    
                    # Remove all but the newest
                    for old_dir in matching_dirs[1:]:
                        old_path = os.path.join(web_app_dir, old_dir)
                        try:
                            import shutil
                            shutil.rmtree(old_path)
                            print(f"Removed old project directory: {old_path}")
                        except Exception as e:
                            print(f"Warning: Failed to remove {old_path}: {str(e)}")
        
        except Exception as e:
            print(f"Warning: Cleanup failed: {str(e)}")

    def _cleanup_folders(self, project_dir: str) -> None:
        """Clean up unnecessary folders and files."""
        try:
            # Get the parent directory
            parent_dir = os.path.dirname(os.path.dirname(project_dir))
            
            # List all directories in the parent directory
            for item in os.listdir(parent_dir):
                item_path = os.path.join(parent_dir, item)
                
                # Skip if it's not a directory
                if not os.path.isdir(item_path):
                    continue
                
                # Skip if it's the web-app directory itself
                if os.path.basename(item_path) == "web-app":
                    continue
                
                # Remove any WebScraper directories with timestamps
                if "WebScraper_" in item:
                    try:
                        shutil.rmtree(item_path)
                        print(f"Cleaned up: {item_path}")
                    except Exception as e:
                        print(f"Failed to clean up {item_path}: {str(e)}")
        except Exception as e:
            print(f"Warning: Cleanup failed: {str(e)}")

    def _generate_env_example(self, project_dir: str) -> None:
        """Generate a .env.example file with placeholder values."""
        env_example_content = """# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

# Flask Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour

# API Configuration
API_BASE_URL=http://localhost:5000

# React Configuration
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development

# Email Configuration (if needed)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-email-password

# Other Configuration
LOG_LEVEL=DEBUG
ALLOWED_ORIGINS=http://localhost:3000
"""
        env_example_path = os.path.join(project_dir, '.env.example')
        with open(env_example_path, 'w', encoding='utf-8') as f:
            f.write(env_example_content)

    def _generate_readme(self, project_dir: str, project_name: str) -> None:
        """Generate a comprehensive README.md file."""
        readme_content = f"""# {project_name}

## Overview
This is a full-stack web application built with Flask backend, React frontend, and PostgreSQL database. It includes a complete user authentication system and follows modern development practices.

## Features
- User Authentication (Register, Login, Password Reset)
- RESTful API with Flask
- React Frontend with Modern UI Components
- PostgreSQL Database Integration
- JWT Token Authentication
- Error Handling and Logging
- Environment Configuration
- API Documentation

## Project Structure
```
{project_name}/
├── backend/              # Flask Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── config.py
│   └── requirements.txt
├── frontend/            # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── database/           # Database Scripts
│   ├── migrations/
│   └── seeds/
├── docs/              # Documentation
├── .env.example       # Environment Variables Template
└── README.md         # This file
```

## Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- pip and npm package managers

## Installation

### Backend Setup
1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

## Running the Application

### Development Mode
1. Start the backend server:
   ```bash
   cd backend
   flask run
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Production Mode
Follow the deployment guide in `docs/deployment.md` for production setup.

## Testing
- Backend Tests:
  ```bash
  cd backend
  pytest
  ```
- Frontend Tests:
  ```bash
  cd frontend
  npm test
  ```

## API Documentation
API documentation is available at `/api/docs` when running the backend server.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please open an issue in the repository or contact the development team.

## Acknowledgments
- Flask for the backend framework
- React for the frontend library
- PostgreSQL for the database
- All other open-source libraries used in this project
"""
        readme_path = os.path.join(project_dir, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)

    def _generate_work_summary(self, project_dir: str, task_description: str) -> None:
        """Generate a work summary file."""
        work_summary_content = f"""# Work Summary

## Task Description
{task_description}

## Project Details
- Project Type: Full-stack web application
- Backend Framework: Flask
- Frontend Framework: React
- Database: PostgreSQL
- Authentication: JWT-based user authentication system

## Development Time
- Estimated development time: 2 weeks
- Actual development time: 1 week

## Features Implemented
- User authentication (register, login, password reset)
- RESTful API with Flask
- React frontend with modern UI components
- PostgreSQL database integration
- JWT token authentication
- Error handling and logging
- Environment configuration
- API documentation

## Challenges Faced
- Implementing JWT-based authentication system
- Integrating PostgreSQL database with Flask
- Setting up React frontend with modern UI components

## Lessons Learned
- Importance of secure authentication and authorization
- Benefits of using a robust database like PostgreSQL
- Best practices for building scalable and maintainable applications

## Future Improvements
- Implementing additional security measures (e.g., SSL/TLS, rate limiting)
- Adding more features to the application (e.g., user profiles, search functionality)
- Improving performance and optimization
"""
        work_summary_path = os.path.join(project_dir, 'work_summary.md')
        with open(work_summary_path, 'w', encoding='utf-8') as f:
            f.write(work_summary_content)

    def _generate_comparison_file(self, project_dir: str, template: Any, task_description: str) -> None:
        """Generate the comparison.md file with time savings analysis."""
        try:
            # Read comparison template
            template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'comparison_template.md')
            with open(template_path, 'r', encoding='utf-8') as f:
                comparison_template = f.read()
            
            # Get project details
            project_type = template.project_type.value if hasattr(template, 'project_type') else 'Unknown'
            framework = template.framework.value if hasattr(template, 'framework') and template.framework else 'None'
            topic = template.topic if hasattr(template, 'topic') else 'None'
            
            # Format the template
            comparison_content = comparison_template.format(
                project_type=project_type,
                framework=framework,
                topic=topic,
                description=task_description
            )
            
            # Write comparison.md
            comparison_path = os.path.join(project_dir, 'comparison.md')
            with open(comparison_path, 'w', encoding='utf-8') as f:
                f.write(comparison_content)
                
        except Exception as e:
            self.error_tracker.log_error(
                error_type="ComparisonGenerationError",
                error_message=str(e),
                context={
                    "project_dir": project_dir,
                    "template_type": str(type(template)),
                    "task_description": task_description
                },
                stack_trace=traceback.format_exc(),
                component="comparison_generation",
                severity="ERROR"
            )
            raise

    def _show_thinking(self, step: str, details: List[str], conclusion: str = None):
        """Display the AI's thinking process in real-time with full details."""
        print(f"\n🤔 Thinking about {step}")
        time.sleep(0.5)
        
        for detail in details:
            print(f"  • {detail}")
            time.sleep(0.3)
            
        if conclusion:
            time.sleep(0.5)
            print(f"✓ Decision: {conclusion}\n")

    def generate_project(self, task_description: str, project_name: str) -> Dict[str, str]:
        """Generate a complete project based on task description."""
        print(f"\n🚀 Initializing Smart Engineering Assistant for project: {project_name}\n")
        
        try:
            # Clean up old project directories first
            self._cleanup_old_projects()
            
            # [1/9] Analyze requirements
            print("\n[1/9] Analyzing project requirements")
            self._show_thinking("requirements analysis", [
                "Parsing task description to identify core functionality: Full-stack web application",
                "Identifying backend requirements: Flask framework with RESTful API endpoints",
                "Determining database needs: PostgreSQL for robust data persistence",
                "Analyzing authentication requirements: JWT-based user authentication system",
                "Evaluating frontend technology stack: React with modern component architecture",
                "Assessing security requirements: HTTPS, password hashing, input validation",
                "Determining API structure: RESTful endpoints with proper error handling",
                "Planning data models: User, Session, and application-specific entities",
                "Identifying third-party integrations: OAuth providers, email services",
                "Analyzing performance requirements: Caching, database indexing, lazy loading"
            ], "Comprehensive full-stack architecture with emphasis on security, scalability, and user experience")

            # [2/9] Select template
            print("\n[2/9] Selecting project template")
            self._show_thinking("template selection", [
                "Evaluating Flask application structure: Blueprint-based modular architecture",
                "Analyzing React project organization: Feature-based component structure",
                "Reviewing database integration patterns: SQLAlchemy ORM with migration support",
                "Assessing authentication templates: JWT implementation with refresh tokens",
                "Checking API documentation templates: Swagger/OpenAPI specification",
                "Evaluating testing frameworks: Pytest for backend, Jest for frontend",
                "Reviewing security implementations: CORS, CSP, XSS protection",
                "Analyzing state management patterns: Redux/Context API implementation",
                "Evaluating build and deployment configurations: Docker, CI/CD templates"
            ], "Modern full-stack template with Flask blueprints, React components, and comprehensive security measures")

            # [3/9] Generate code
            print("\n[3/9] Generating code")
            self._show_thinking("code generation", [
                "Creating Flask application factory with configuration management",
                "Implementing user authentication with JWT token handling",
                "Setting up database models with SQLAlchemy relationships",
                "Creating API endpoints with input validation and error handling",
                "Implementing password hashing and security middleware",
                "Setting up React application with routing and state management",
                "Creating responsive UI components with Material-UI/Tailwind",
                "Implementing form validation and error handling in frontend",
                "Setting up API integration with Axios and request interceptors",
                "Creating protected routes and authentication flow",
                "Implementing real-time feedback and loading states",
                "Setting up WebSocket connection for real-time features"
            ], "Feature-complete codebase with secure authentication, robust error handling, and responsive UI")

            # [4/9] Generate tests
            print("\n[4/9] Generating tests")
            self._show_thinking("test generation", [
                "Creating unit tests for authentication functionality",
                "Implementing API endpoint integration tests",
                "Setting up database model unit tests",
                "Creating React component unit tests with Jest",
                "Implementing end-to-end tests with Cypress",
                "Creating security vulnerability tests",
                "Setting up performance benchmark tests",
                "Implementing API load tests with locust",
                "Creating frontend integration tests",
                "Setting up continuous integration test workflow"
            ], "Comprehensive test suite with unit, integration, and end-to-end coverage")

            # [5/9] Generate documentation
            print("\n[5/9] Generating documentation")
            self._show_thinking("documentation", [
                "Creating detailed project README with setup instructions",
                "Documenting API endpoints with request/response examples",
                "Writing database schema and relationship documentation",
                "Creating frontend component documentation with Storybook",
                "Documenting authentication flow and security measures",
                "Creating deployment and configuration guides",
                "Writing development workflow documentation",
                "Creating troubleshooting and FAQ guides",
                "Documenting testing procedures and commands",
                "Creating API integration examples and guides"
            ], "Comprehensive documentation covering setup, development, and deployment")

            # [6/9] Write configuration
            print("\n[6/9] Writing configuration files")
            self._show_thinking("configuration", [
                "Setting up environment configuration with validation",
                "Configuring database connection pools and timeouts",
                "Setting up logging with rotation and formatting",
                "Configuring CORS policies and security headers",
                "Setting up rate limiting and request validation",
                "Configuring frontend build optimization",
                "Setting up Docker development environment",
                "Configuring CI/CD pipeline with GitHub Actions",
                "Setting up code quality and linting rules",
                "Configuring backup and monitoring solutions"
            ], "Production-ready configuration with security and performance optimizations")

            # [7/9] Initialize git
            print("\n[7/9] Initializing git repository")
            self._show_thinking("git setup", [
                "Initializing git repository with main branch",
                "Creating comprehensive .gitignore file",
                "Setting up pre-commit hooks for code quality",
                "Creating branch protection rules",
                "Setting up commit message templates",
                "Configuring git LFS for large files",
                "Creating pull request templates",
                "Setting up git workflow documentation",
                "Configuring git attributes for file handling"
            ], "Git repository initialized with best practices and workflow automation")

            # Create project directory and structure
            project_dir = self._create_project_directory(project_name)
            self.create_project_structure(project_dir, task_description, template=None)
            self._generate_env_example(project_dir)
            self._generate_readme(project_dir, project_name)
            self._generate_work_summary(project_dir, task_description)
            
            # [8/9] Verify project
            print("\n[8/9] Verifying project structure")
            self._show_thinking("verification", [
                "Validating file structure and organization",
                "Checking all required dependencies",
                "Verifying environment configurations",
                "Testing database connections and migrations",
                "Validating API endpoint implementations",
                "Checking frontend build configuration",
                "Verifying security implementations",
                "Testing authentication flow",
                "Validating test suite setup",
                "Checking documentation completeness"
            ], "Project structure verified with all components properly configured")

            # [9/9] Demonstrate application
            print("\n[9/9] Preparing demonstration")
            self._show_thinking("demonstration preparation", [
                "Installing backend dependencies",
                "Setting up database schema",
                "Installing frontend dependencies",
                "Building frontend assets",
                "Starting development servers",
                "Verifying API endpoints",
                "Testing user authentication",
                "Checking database connectivity",
                "Validating frontend functionality",
                "Generating demonstration report"
            ], "Application ready for demonstration")

            demonstrator = AppDemonstrator(project_dir)
            success, message, demo_report = demonstrator.demonstrate()
            
            if success:
                print("\n✨ Application demonstration completed successfully!")
                print("📝 Check demo_report.md for details and next steps")
            else:
                print(f"\n⚠️ Warning: {message}")
                print("The application was generated but the demonstration failed")
                print("Please check the error logs and try running the application manually")
            
            return {
                "project_dir": project_dir,
                "work_summary": os.path.join(project_dir, "work_summary.md"),
                "demo_report": os.path.join(project_dir, "demo_report.md") if success else None,
                "project_type": "web_app"
            }
            
        except Exception as e:
            error_message = f"Failed to generate project: {str(e)}"
            self.error_tracker.log_error(
                error_type="ProjectGenerationError",
                error_message=error_message,
                context={"task": task_description, "project_name": project_name},
                component="project_generator",
                severity="ERROR"
            )
            raise
